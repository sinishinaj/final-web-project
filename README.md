# Photo Tech World — Selenium Test Suite

Automated end-to-end tests for the Photo Tech World web application, written with **Python 3**, **pytest**, and **Selenium WebDriver**.

---

## Test Structure

Every test follows the **Setup → Action → Assertion** pattern:

- **Setup** — brings the browser into the required starting state (e.g. logged in, correct page loaded).
- **Action** — interacts with the UI exactly as a real user would (clicking, typing, submitting).
- **Assertion** — verifies that the DOM reflects the expected outcome.

This separation keeps each test focused on a single behaviour, makes failures easy to diagnose, and ensures tests are independent of one another.

---

## Login Helper — `do_login()`

Because login is a prerequisite for most tests, the steps are extracted into a plain helper function `do_login(driver, base_url)` rather than duplicated in every test. It navigates to the page, fills in the credentials, clicks the login button, and waits until `#app` is visible before returning. Any test that needs an authenticated session simply calls `do_login()` at the top, keeping the test body focused on the scenario it actually covers.

---

## Tests

### `test_login_reveals_app`

Verifies that submitting valid credentials hides the login page and reveals the main application.

| Phase | What happens |
|-------|-------------|
| **Setup** | Page is loaded and credentials are ready to be entered. |
| **Action** | Username and password are typed into their inputs; the Login button is clicked. |
| **Assertion** | The `#app` element no longer carries the `hidden` class, confirming the main application is visible. |

---

### `test_contact_form`

Verifies that filling in the contact form with valid data and submitting it shows a success message.

| Phase | What happens |
|-------|-------------|
| **Setup** | `do_login()` is called to reach the authenticated state; the Contact nav button is clicked and the contact section is waited on. |
| **Action** | Name, email, phone, and message fields are filled in; the Submit button is clicked. |
| **Assertion** | The `#formSuccess` element contains the text `"Message sent successfully!"`. |

---

### `test_logout_hides_app`

Verifies that clicking the Logout button returns the application to the logged-out state.

| Phase | What happens |
|-------|-------------|
| **Setup** | `do_login()` is called so the app is visible and the logout button is accessible. |
| **Action** | The `.logout` button inside `#app` is clicked, triggering a full page reload. |
| **Assertion** | After the reload, `#app` has the `hidden` class again, confirming the user has been signed out. |

---

## Running the Tests

```bash
# First-time setup
sudo apt install -y python3.12-venv python3-pip
bash setup.sh

# Run all tests (from a graphical terminal session)
source venv/bin/activate
pytest test_webpage.py -v
```

> **Note:** Chrome opens a visible browser window during the test run. The terminal must belong to a graphical desktop session (`DISPLAY` or `WAYLAND_DISPLAY` must be set). Running from a TTY without a display will cause Chrome to crash on startup.
