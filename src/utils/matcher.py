class MatcherUtil:
    @staticmethod
    def is_company_name_match_developer_name(company_name: str, developer_name: str) -> bool:
        special_chars = ",./<>?;':\"[]\{}|`~!@#$%^&*()_+-= "
        developer = developer_name.lower()
        company = company_name.lower()
        company_name_parts = company.split(" ")
        developer_parts = developer.split(" ")
        stripped_developer_parts = {
            part.strip(special_chars) for part in developer_parts
        }
        stripped_company_parts = {
            part.strip(special_chars) for part in company_name_parts
        }
        return stripped_company_parts.issubset(stripped_developer_parts)
