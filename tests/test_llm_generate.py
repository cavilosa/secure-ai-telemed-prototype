from services.llm_service import llm_service, LLMService
import pytest
from pytest_mock import MockerFixture 

class TestLLMService:
    """
    Test suite for the LLMService class.
    """

    def test_generate_success_happy_path(self, mocker: MockerFixture):
        """
        Tests the successful generation of text by mocking the model.
        
        - The 'mocker' is passed in as an argument by pytest.
        """

        fake_prompt = "Hello AI"
        fake_response_text = "Hello AI, this is a predictable test response."
        fake_model_output = [{'generated_text': fake_response_text}]

        mocker.patch(
            'services.llm_service.llm_service.generator',
            return_value=fake_model_output
        )

        actual_result = llm_service.generate(fake_prompt)

        assert actual_result == fake_response_text

    @pytest.mark.parametrize("bad_input", [
        None,       # Test for None
        123,        # Test for an integer
        [],         # Test for a list
        {"a": 1}    # Test for a dictionary
    ])
    def test_generate_handles_bad_inputs(self, bad_input):
        """
        Tests that the service doesn't crash when given various invalid inputs.
        """
        result = llm_service.generate(bad_input)

        # ASSERT
        # The function should catch the internal error and return our friendly message.
        expected_error_msg = "Sorry, an error occurred while generating the text."
        assert result == expected_error_msg


    def test_generate_when_model_fails_to_load(self, mocker: MockerFixture):
        """
        Tests the service's graceful failure mode when the model is None.
        """
        mocker.patch.object(llm_service, 'generator', None)

        fail_llm_return = llm_service.generate("any prompt")
        
        expected_error_msg = "Sorry, the text generation service is currently unavailable."
        assert fail_llm_return == expected_error_msg

