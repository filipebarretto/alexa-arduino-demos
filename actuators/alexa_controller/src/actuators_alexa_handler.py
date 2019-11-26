# -*- coding: utf-8 -*-

import json
import logging
import boto3
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
AbstractRequestHandler, AbstractExceptionHandler,
AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
get_plain_text_content, get_rich_text_content)

from ask_sdk_model.interfaces.display import (
ImageInstance, Image, RenderTemplateDirective, ListTemplate1,
BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response

from custom_modules import data, util
    

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



iot = boto3.client('iot-data', region_name='us-east-1')
colors = {"vermelha": "red", "vermelho": "red", "amarela": "yellow", "amarelo": "yellow", "verde": "green"};


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        handler_input.response_builder.speak(data.WELCOME_MESSAGE).ask(
                                                                       data.HELP_MESSAGE)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(
                                                     handler_input.request_envelope))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session
        
        handler_input.response_builder.speak(
                                             data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        handler_input.response_builder.speak(
                                             data.EXIT_SKILL_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


class LightOnHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("light_on")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LightOnHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        light_slot = util.get_slots(handler_input.request_envelope.request.intent.slots)[0]
        command = data.COLORS[light_slot] + "_light_on"
        logger.info(command)
        util.iot_command(command)
        
        rsp = random.choice(data.TURNING_LIGHT_ON) + light_slot + "."
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class LightOffHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("light_off")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LightOffHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        light_slot = util.get_slots(handler_input.request_envelope.request.intent.slots)[0]
        command = data.COLORS[light_slot] + "_light_off"
        logger.info(command)
        util.iot_command(command)
        
        rsp = random.choice(data.TURNING_LIGHT_OFF) + light_slot + "."
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class LightsOnHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("lights_on")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LightsOnHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        lights_str = ""
        light_slots = util.get_slots(handler_input.request_envelope.request.intent.slots)
        count = 1
        for light_slot in light_slots:
            command = data.COLORS[light_slot] + "_light_on"
            logger.info(command)
            util.iot_command(command)
            lights_str += light_slot + (", " if count < len(light_slots) - 1 else (" e " if count < len(light_slots) else "."))
            count += 1

        
        rsp = random.choice(data.TURNING_LIGHT_ON) + lights_str
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response



class LightsOffHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("lights_off")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LightsOffHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        lights_str = ""
        light_slots = util.get_slots(handler_input.request_envelope.request.intent.slots)
        count = 1
        for light_slot in light_slots:
            command = data.COLORS[light_slot] + "_light_of"
            logger.info(command)
            util.iot_command(command)
            lights_str += light_slot + (", " if count < len(light_slots) - 1 else (" e " if count < len(light_slots) else "."))
            count += 1
        
        
        rsp = random.choice(data.TURNING_LIGHT_OFF) + lights_str
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class AllLightsOnHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("all_lights_on")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AllLightsOnHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        util.iot_command("red_light_on")
        util.iot_command("green_light_on")
        util.iot_command("yellow_light_on")
        
        rsp = random.choice(data.TURNING_ALL_LIGHTS_ON)
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response



class AllLightsOffHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("all_lights_off")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AllLightsOffHandler")
        attr = handler_input.attributes_manager.session_attributes
        
        util.iot_command("red_light_off")
        util.iot_command("green_light_off")
        util.iot_command("yellow_light_off")
        
        rsp = random.choice(data.TURNING_ALL_LIGHTS_OFF)
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class TurnOnFavoriteColorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("favorite_color_on")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In TurnOnFavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        favorite_color = attr["favorite_color"] or ""
        
        response_builder = handler_input.response_builder
        
        if favorite_color is not "":
            command = favorite_color + "_light_on"
            logger.info(command)
            util.iot_command(command)
        
            rsp = random.choice(data.TURNING_FAVORITE_LIGHT_ON)
        
            response_builder = handler_input.response_builder
            response_builder.speak(rsp)
            response_builder.ask(rsp)
        else:
            rsp = random.choice(data.UNDEFINED_FAVORITE_LIGHT)
            
            attr["state"] = "waiting_define_favorite_color"
            
            response_builder = handler_input.response_builder
            response_builder.speak(rsp)
            response_builder.ask(rsp)
        
        
        return response_builder.response
        

class YesDefineFavoriteColorHandler(AbstractRequestHandler):
    """Handler for yes to get more info intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and attr["state"] == "waiting_define_favorite_color")
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesDefineFavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "waiting_favorite_color"
        
        response_builder = handler_input.response_builder
        rsp = random.choice(data.WHICH_FAVORITE_COLOR)
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class NoDefineFavoriteColorHandler(AbstractRequestHandler):
    """Handler for yes to get more info intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and attr["state"] == "waiting_define_favorite_color")
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoDefineFavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = ""
        
        response_builder = handler_input.response_builder
        rsp = random.choice(data.WHICH_FAVORITE_COLOR)
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class SetFavoriteColorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("color_name")(handler_input) and attr["state"] == "waiting_favorite_color")
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = ""
        
        light_slot = util.get_slots(handler_input.request_envelope.request.intent.slots)[0]
        attr["favorite_color"] = data.COLORS[light_slot]
        
        response_builder = handler_input.response_builder
        rsp = (random.choice(data.FAVORITE_COLOR_SAVED)).format(light_slot)
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class RegisterFavoriteColorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("register_favorite_color")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "waiting_favorite_color"

        response_builder = handler_input.response_builder
        rsp = random.choice(data.WHICH_FAVORITE_COLOR)
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class ForgetFavoriteColorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("forget_favorite_color")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ForgetFavoriteColorHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        attr["favorite_color"] = ""
        
        response_builder = handler_input.response_builder
        rsp = random.choice(data.FORGETTING_FAVORITE_COLOR)
        response_builder.speak(rsp)
        response_builder.ask(rsp)
        
        return response_builder.response


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                                                              cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)
            
            return response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.
        2018-May-01: AMAZON.FallackIntent is only currently available in
        en-US locale. This handler will not be triggered except in that
        locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        handler_input.response_builder.speak(
                                             data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)
                                             
        return handler_input.response_builder.response


# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
        The interceptor is used to cache the handler response that is
        being sent to the user. This can be used to repeat the response
        back to the user, in case a RepeatIntent is being used and the
        skill developer wants to repeat the same information back to
        the user.
        """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
        This handler catches all kinds of exceptions and prints
        the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        
        speech = "Ops! Tivemos um problema. Você pode repetir?"
        handler_input.response_builder.speak(speech).ask(speech)
        
        return handler_input.response_builder.response

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
                                                  handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))



# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RepeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())


# Add all request handlers to the skill.
sb.add_request_handler(LightOnHandler())
sb.add_request_handler(LightOffHandler())
sb.add_request_handler(LightsOnHandler())
sb.add_request_handler(LightsOffHandler())
sb.add_request_handler(AllLightsOnHandler())
sb.add_request_handler(AllLightsOffHandler())

sb.add_request_handler(RegisterFavoriteColorHandler())
sb.add_request_handler(SetFavoriteColorHandler())
sb.add_request_handler(TurnOnFavoriteColorHandler())
sb.add_request_handler(YesDefineFavoriteColorHandler())
sb.add_request_handler(NoDefineFavoriteColorHandler())
sb.add_request_handler(ForgetFavoriteColorHandler())


# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
