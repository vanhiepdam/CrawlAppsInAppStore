from src.utils.matcher import MatcherUtil
import pytest


class TestMatcherUtil:
    @pytest.mark.parametrize(
        "company_name, developer_name",
        [
            ("netflix", "Netflix"),
            ("netflix", "Netflix, Inc."),
            ("Netflix", "Netflix"),
            ("Netflix", "Netflix, Inc."),
            ("Netflix", "netflix"),
            ("Netflix", "netflix, Inc."),
            ("netflix", "Netflix +"),
        ]
    )
    def test_is_company_name_match_developer_name__match(self, company_name, developer_name):
        # Act
        result = MatcherUtil.is_company_name_match_developer_name(
            company_name, developer_name
        )

        # Assert
        assert result is True

    @pytest.mark.parametrize(
        "company_name, developer_name",
        [
            ("netflixx", "Netflix"),
            ("netflix", "Netfli"),
            ("netflix", "Netfli, Inc"),
            ("net flix", "Netflix, Inc"),
            ("netfli", "Netflix, Inc"),
        ]
    )
    def test_is_company_name_match_developer_name__not_match(self, company_name, developer_name):
        # Act
        result = MatcherUtil.is_company_name_match_developer_name(
            company_name, developer_name
        )

        # Assert
        assert result is False
