"""lambda_function.py: demo Alexa skill."""
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler)
from ask_sdk_core.utils import (
    is_intent_name, is_request_type)
import random

COLORS = ("orange", "purple", "yellow", "green")


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""

    def can_handle(self, handler_input):
        """Can handle or not."""
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """Speak our ."""
        print("In LaunchRequestHandler")
        # we expect a response, so we need to include a reprompt with `ask`
        (handler_input.response_builder
            .speak("What is your favorite color? ")
            .ask("please tell me your favorite color. "))
        return handler_input.response_builder.response


class ColorIntentHandler(AbstractRequestHandler):
    """Handler for ColorIntent."""

    def can_handle(self, handler_input):
        """Can handle or not."""
        return (is_request_type("IntentRequest")(handler_input) and
                is_intent_name("ColorIntent")(handler_input))

    def handle(self, handler_input):
        """Compare slot value to COLORS, and generate a response."""
        print("In ColorIntentHandler")
        slot_color = handler_input.request_envelope.request.intent.slots[
            "color"].value
        if random.randrange(2) == 1:
            message = "I like " + slot_color + ", too. "
        else:
            # note: I didn't bother to check that `choice`!= `slot_color`
            message = "I think " + random.choice(COLORS) + " is a better color"
        (handler_input.response_builder
            .speak(message)
            .set_should_end_session(True))
        return handler_input.response_builder.response


class StopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel, Stop intents."""

    def can_handle(self, handler_input):
        """Can handle or not."""
        return (is_request_type("IntentRequest")(handler_input) and
                (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                 is_intent_name("AMAZON.StopIntent")(handler_input)))

    def handle(self, handler_input):
        """Handle response."""
        print("In StopIntentHandler")
        (handler_input.response_builder
            .speak("Ok. Bye.")
            .set_should_end_session(True))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""

    def can_handle(self, handler_input):
        """Can handle or not."""
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        """Handle response."""
        print("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(
            handler_input.request_envelope.request))
        return handler_input.response_builder.response


# Exception Handler class
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.

    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope.
    """

    def can_handle(self, handler_input, exception):
        """Can handle or not."""
        return True

    def handle(self, handler_input, exception):
        """Handle response."""
        # type: (HandlerInput, Exception) -> Response
        print(exception, exc_info=True)
        print("Original request was {}".format(
            handler_input.request_envelope.request))
        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


# ---------------------------------------------------- #
sb = SkillBuilder()

# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ColorIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
