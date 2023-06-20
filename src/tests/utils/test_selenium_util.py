from unittest.mock import Mock

from src.utils.selenium import SeleniumUtil


class TestSeleniumUtil:
    def test_scroll_to_bottom_infinite__no_scroll(self):
        # Arrange
        driver = Mock()
        driver.execute_script = Mock(return_value=100)

        # Act
        SeleniumUtil.scroll_to_bottom_infinite(driver)

        # Assert
        driver.execute_script.assert_called_once_with(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def test_scroll_to_bottom_infinite__scroll_once(self):
        # Arrange
        driver = Mock()
        driver.execute_script = Mock(side_effect=[100, 200])

        # Act
        SeleniumUtil.scroll_to_bottom_infinite(driver)

        # Assert
        driver.execute_script.assert_called_with("window.scrollTo(0, document.body.scrollHeight);")
        assert driver.execute_script.call_count == 2

    def test_scroll_to_bottom_infinite__scroll_twice(self):
        # Arrange
        driver = Mock()
        driver.execute_script = Mock(side_effect=[100, 200, 300])

        # Act
        SeleniumUtil.scroll_to_bottom_infinite(driver)

        # Assert
        driver.execute_script.assert_called_with("window.scrollTo(0, document.body.scrollHeight);")
        assert driver.execute_script.call_count == 3

    def test_scroll_to_bottom_infinite__scroll_twice_with_sleep(self):
        # Arrange
        driver = Mock()
        driver.execute_script = Mock(side_effect=[100, 200, 300])

        # Act
        SeleniumUtil.scroll_to_bottom_infinite(driver, sleep_seconds=3)

        # Assert
        driver.execute_script.assert_called_with("window.scrollTo(0, document.body.scrollHeight);")
        assert driver.execute_script.call_count == 3
