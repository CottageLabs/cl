<!-- for clearer nester list appearance -->
<style>
.lower_roman+ol, .lower_roman+ul {list-style-type: lower-roman;}
.upper_roman+ol, .upper_roman+ul {list-style-type: upper-roman;}
.lower_alpha+ol, .lower_alpha+ul {list-style-type: lower-alpha;}
.upper_alpha+ol, .upper_alpha+ul {list-style-type: upper-alpha;}
.lower_greek+ol, .lower_greek+ul {list-style-type: lower-greek;}
.lower_latin+ol, .lower_latin+ul {list-style-type: lower-latin;}
.upper_latin+ol, .upper_latin+ul {list-style-type: upper-latin;}
.none+ol, .none+ul {list-style-type:none;}
.disc+ol, .disc+ul {list-style-type:disc;}
.circle+ol, .circle+ul {list-style-type:circle;}
.square+ol, .square+ul {list-style-type:square;}
.decimal+ol, .decimal+ul {list-style-type:decimal;}
.decimal_leading_zero+ol, .decimal_leading_zero+ul {list-style-type:decimal-leading-zero;}
</style>

<style>
h1 {margin-top: 2em;}
h1:first-child {margin-top: 0;}
h2 {margin-top: 1.5em;}
</style>

<h1 style="margin-top:0;">Testing</h1>
- lets new people contribute much more easily - they can tell what the code is supposed to do
- reduces "oh shit I broke the software" moments - tests can be run automatically before deploying new changes and when new features are written
- lets multiple developers work at the same time without fear of breaking each other's code
- increases resilience - if somebody leaves, it's much easier for another to pick up what they were doing
- lets developers get back into (an area of) the code that they haven't touched for months - as long as their newest changes don't break the tests, all is well

# ContentMine Goes Testing

> *"Functional tests test the application from the outside, from the point of view of the user. Unit tests test the application from the inside, from the point of view of the programmer."*

<div class="upper_alpha"></div><!-- classes defined at top of page body -->
1. Functional tests (a.k.a. "black box tests") first. ContentMine is made of different programs which talk to each other. The important thing is to test the boundaries so a developer always knows if they broke the way the program interacts with others. These need to cover 100% of the points of interaction - not hard as there aren't that many endpoints in a web app.

2. Unit tests - ideally we will have 100% coverage. Aiming for 90% (which means we will likely achieve 60-70% initially and improve it as it goes more stable).

3. Continuous integration - we will use <http://drone.io> like this:
    1. branch from master, giving it a sensible name (include github issue number you're working on if there is one)
    2. write 1+ tests, check they fail
    3. write code to satisfy tests
    4. push your branch up
    5. Drone will run all tests and email the dev team with the result (you can follow on the Drone website too).
    6. If build passes, checkout master, git pull and merge your new branch.
    7. Push master.
    8. Drone will run all the tests, email the dev team with the result, and automatically deploy the new master on the contentmine server.
    
    As you can see you are also free to commit very fast bugfixes or typo fixes directly to master - when you push the tests will run anyway.
    This setup is quite flexible - do whatever you want with git, but don't deploy manually - let Drone do it.
    
# Testing guidelines

## Development Workflow

1. Write a functional test. **What** does the new feature, ultimately, need to do from the PoV of potential users?
2. Write a few unit tests. **How** do you think the code should achieve the desired effect?
3. Write some code to satisfy unit tests. If they fail, but go further than the initial failures, think of what other unit tests you could write - then write more app code.
4. Once all unit tests pass, run the functional tests. If they fail but go further than initially expected, think of what you could add to them to fully test the app from a user's PoV.

When you're happy and all tests pass, you're done with this feature. *This is not waterfall - once you've written down your initial expectations in a first batch of failing tests, go back and forth between tests and app code as much as you need to - follow your thoughts. Do not force yourself to follow a rigid workflow unless you feel you need it.*

If you feel like some elaborating on this topic, read

<http://chimera.labs.oreilly.com/books/1234000000754/ch03.html#_unit_tests_and_how_they_differ_from_functional_tests> .

## Functional tests

### HTML pages
Use Selenium. HTML is meant for human consumption, and Selenium is focussed on testing exactly that. Basic example: <https://github.com/emanuil-tolev/obey_the_testing_goat/blob/master/simple_selenium_example.py>

Even if you don't think you need it initially (e.g. "For now I just want to know if this string is present in this page."), USE SELENIUM. You don't just want to know if a string is present, you want to know if the string is there when opened in a modern graphical browser which makes a ton of assumptions and has default content negotiation and so on.

#### Javascript in HTML pages during functional tests
TODO

### API endpoints
Use the simplest possible way of making requests. In Python, this is the requests library. Just load up the JSON responses of the API and make assertions about the contents.

## Unit tests

Mock external dependencies on API-s. Use suitable content in functional tests to make sure external API-s are working.

Keep mocks as simple as possible - having to keep state is very likely very bad. 99% of the time mocks will just return predetermined fixed strings.

### Data storage
Mock the data storage - just use fixtures! Elasticsearch returns JSON objects anyway, how hard is it to save a couple of JSON fixtures and load them at setup?

Do not mock the data storage if you're testing data access code, that's just what-the-heck.

### Javascript
TODO

## Practicalities

We're using the py.test framework <http://pytest.org/latest/getting-started.html#our-first-test-run> . This has been selected over unittest for its simpler assertions (tests more readable and pythonic) and advanced introspection (so you don't have to print intermediate values in the failure messages explicitly, useful on occasion.)

TODO: link to app setup guide which should include instructions on how to run all tests, run functional tests separately, run unit tests separately and run one single file of tests.



Original Title: ContentMine Testing Strategy
Original Author: emanuil
Tags: contentmine, testing, tdd, drone, selenium, blog-driven development, emanuil, mark
Created: 2014-06-15 1502
Last Modified: 2014-06-15 1828
