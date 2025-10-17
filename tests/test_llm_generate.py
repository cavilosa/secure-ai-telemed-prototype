from services.llm_service import llm_service
import pytest

# You will need to have the 'pytest-mock' library installed for this.
# It provides the 'mocker' fixture.

class TestLLMService:
    """
    Test suite for the LLMService class.
    """

    def __init__(self):
        self.mocker

    def test_generate_success_happy_path(self, mocker):
        """
        Tests the successful generation of text when the model behaves as expected.
        This is your 'test_mock_generation'.
        """

        fake_prompt = "Hello AI"
        fake_response_text = "Hello AI, this is a predictable test response."
        fake_model_output = [{'generated_text': fake_response_text}]

        mocker.patch(
            'services.llm_service.llm_service.generator',
            return_value=fake_model_output             
        )

        # 3. Call the real function you are testing
        actual_result = llm_service.generate(fake_prompt)

        # 4. Assert that the result is what you expected
        assert actual_result == fake_response_text

    @pytest.mark.parametrize("bad_input", [None, 123, "", []])
    def test_generate_handles_bad_inputs(self, bad_input):
        """
        Tests that the service doesn't crash and returns a sensible default
        when given invalid input. This is your 'test_bad_inputs'.
        """
        # HINT: Call llm_service.generate() with each 'bad_input' and
        # assert that the function returns a string and doesn't raise an error.
        pass

    def test_generate_when_model_fails_to_load(self, mocker):
        """
        Tests the service's catastrophic failure mode where the model is None.
        This is your 'test_catastrophic_failuer'.
        """
        # HINT: Use mocker.patch.object(llm_service, 'generator', None)
        # to simulate the model failing to load during startup.
        # Then, assert that calling llm_service.generate() returns the specific
        # error message: "Sorry, the text generation service is currently unavailable."
        pass
