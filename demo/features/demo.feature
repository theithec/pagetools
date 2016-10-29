Feature: Demo is running

  Scenario Outline: visit the demo home page
    Given site has content
    When i visit the url "<url>"
    Then the title should be "<title>"

    Examples: Pages
        | url      | title   |
        | /        | Welcome |
        | /polls    | Polls   |

