# Use an absolute import from the project root
from services.redaction import redact_email, redact_phone_number

class TestReduction:
    def test_redact_email(self):
        # Test cases with expected redactions
        # Corrected the expected output to [REDACTED EMAIL]
        test_cases = [
            ("Contact me at cavilosa33@gnaui.com", "Contact me at [REDACTED EMAIL]"),
            ("My email is cavilosa+33@gnai.uk.com", "My email is [REDACTED EMAIL]"),
            ("Emails: servio.nfkjd@ukr.com", "Emails: [REDACTED EMAIL]"),
            ("Reach out at vfdj_vfndj+54@cavillosa.com", "Reach out at [REDACTED EMAIL]"),
            ("No email here!", "No email here!"),
            ("Multiple emails: vfdj_vfndj+54@cavillosa.com, servio.nfkjd@ukr.com",
             "Multiple emails: [REDACTED EMAIL], [REDACTED EMAIL]"),
            ("Edge case: .@example.com", "Edge case: .@example.com"), # Should not redact invalid email
            ("Another edge case: user@.com", "Another edge case: user@.com"), # Should not redact invalid email
            ("Invalid email: user@com", "Invalid email: user@com"),
            ("Invalid email: user@domain..com", "Invalid email: user@domain..com"),
            ("Invalid email: user@domain,com", "Invalid email: user@domain,com"),
            ("Invalid email: user@domain", "Invalid email: user@domain"),
            ("Invalid email: @domain.com", "Invalid email: @domain.com"),
            ("Invalid email: userdomain.com", "Invalid email: userdomain.com"),
            ("Long email: " + "a"*64 + "@" + "b"*63 + ".com", "Long email: [REDACTED EMAIL]"),
            ("Short email: a@b.c", "Short email: [REDACTED EMAIL]")
        ]

        for input_text, expected_output in test_cases:
            assert redact_email(input_text) == expected_output


    def test_redact_phone_number(self):
        # Test cases with expected redactions
        test_cases = [
            ("Call me at (123) 456-7890", "Call me at [REDACTED PHONE]"),
            ("My number is 123-456-78-90", "My number is 123-456-78-90"), # Invalid format
            ("Reach me at 1234567890", "Reach me at [REDACTED PHONE]"),
            ("International: +1 (123) 456-7890", "International: [REDACTED PHONE]"),
            ("No phone number here!", "No phone number here!"),
            ("Multiple numbers: (123) 456-7890, 987-654-3210",
             "Multiple numbers: [REDACTED PHONE], [REDACTED PHONE]"),
            ("Edge case: 1234567", "Edge case: 1234567"),  # Should not redact, too short
            ("Another edge case: 123-45-6789", "Another edge case: 123-45-6789"),  # Should not redact
            ("Invalid number: 12-3456-7890", "Invalid number: 12-3456-7890"),  # Should not redact
            ("Long number: 1234567890123", "Long number: 1234567890123"),  # Should not redact
            ("Short number: 123456", "Short number: 123456"),  # Should not redact
            ("Number with country code: 1-123-456-7890", "Number with country code: [REDACTED PHONE]"),
            ("Number with dots: 123.456.7890", "Number with dots: [REDACTED PHONE]"),
            ("Number with spaces: 123 456 7890", "Number with spaces: [REDACTED PHONE]"),
            ("Mixed format: (123)456-7890", "Mixed format: [REDACTED PHONE]"),
            ("Another mixed format: 123-456 7890", "Another mixed format: [REDACTED PHONE]"),
            ("Just digits: 11234567890", "Just digits: [REDACTED PHONE]"),  # 11 digits starting with '1'
            ("Just digits: 1234567890", "Just digits: [REDACTED PHONE]"),   # 10 digits
        ]

        for input_text, expected_output in test_cases:
            assert redact_phone_number(input_text) == expected_output
