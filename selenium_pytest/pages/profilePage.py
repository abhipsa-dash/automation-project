"""Contains all XPaths and Selenium methods related to the LinkedIn profile page."""

import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_pytest.utils.Common import robust_click

_SYSTEM_DIR       = os.path.join(os.path.dirname(__file__), "..", "..", "data", "selpy_app", "system")
_EDU_HTML_PATH    = os.path.join(_SYSTEM_DIR, "education_form.html")
_EDU_XPATH_CACHE  = os.path.join(_SYSTEM_DIR, "education_xpaths.json")
_ABOUT_HTML_PATH  = os.path.join(_SYSTEM_DIR, "about_form.html")
_ABOUT_XPATH_CACHE = os.path.join(_SYSTEM_DIR, "about_xpaths.json")


class ProfilePage:
    def __init__(self, driver):
        self.driver = driver

    # ── Navigation ────────────────────────────────────────────────────────────
    menu_icon_xpath          = "//button[contains(., 'Me')]"
    view_profile_xpath       = "//a[normalize-space()='View profile']"

    # ── Intro / headline edit modal ───────────────────────────────────────────
    edit_pencil_icon_xpath   = "//a[@aria-label='Edit profile']"
    headline_textbox_xpath   = "//div[@role='textbox']"
    industry_textbox_xpath   = "//input[@aria-label='Industry*']"
    save_button_xpath        = "//button[normalize-space()='Save']"

    # ── About section ─────────────────────────────────────────────────────────
    add_about_button_xpath   = "//button[contains(@aria-label,'Add about')]"
    edit_about_button_xpath  = "//a[@aria-label='Edit about']"
    about_textbox_xpath      = "//div[@data-testid='ui-core-tiptap-text-editor-wrapper']"
    about_save_xpath         = "//button[@aria-label='Save about']"

    # ── Education section ─────────────────────────────────────────────────────
    add_education_xpath      = "//a[@aria-label='Add education']"
    edu_school_xpath         = "//input[@id='education-school-name']"
    edu_degree_xpath         = "//input[@id='education-degree']"
    edu_field_xpath          = "//input[@id='education-field-of-study']"
    edu_start_year_xpath     = "//select[@id='education-start-year']//option[@value='{year}']"
    edu_end_year_xpath       = "//select[@id='education-end-year']//option[@value='{year}']"
    edu_save_xpath           = "//button[@aria-label='Save education']"

    # ── Skills section ────────────────────────────────────────────────────────
    add_skill_xpath          = "//button[contains(@aria-label,'Add skill')]"
    skill_name_xpath         = "//input[@id='skill-name']"
    skill_save_xpath         = "//button[@aria-label='Save skill']"

    # ── Projects section ──────────────────────────────────────────────────────
    add_project_xpath        = "//button[contains(@aria-label,'Add project')]"
    project_name_xpath       = "//input[@id='project-name']"
    project_desc_xpath       = "//textarea[@id='project-description']"
    project_url_xpath        = "//input[@id='project-url']"
    project_save_xpath       = "//button[@aria-label='Save project']"

    # ── Add section button (opens the section picker) ────────────────────────
    add_section_button_xpath = "//button[contains(.,'Add section')]"

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _wait(self, timeout: int = 15):
        return WebDriverWait(self.driver, timeout)

    def _clear_and_type(self, xpath: str, text: str):
        el = self._wait().until(EC.element_to_be_clickable((By.XPATH, xpath)))
        el.click()
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        el.send_keys(text)

    # ── Navigation methods ────────────────────────────────────────────────────

    def _profile_slug(self):
        current = self.driver.current_url
        if "/in/" in current:
            return current.split("/in/")[1].rstrip("/").split("/")[0]
        return None

    def go_to_profile(self):
        slug = self._profile_slug()
        if slug:
            self.driver.get(f"https://www.linkedin.com/in/{slug}/")
        else:
            self.click_menu_icon()
            self.click_view_profile()
            return
        self._wait(20).until(EC.url_contains("/in/"))
        time.sleep(2)

    def _scroll_to(self, xpath: str):
        el = self._wait().until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.5)
        return el

    def click_menu_icon(self):
        # Ensure we are on the feed page so the standard navbar is visible
        if "/feed" not in self.driver.current_url:
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
        robust_click(self, (By.XPATH, self.menu_icon_xpath)).click()
        self._wait().until(EC.visibility_of_element_located((By.XPATH, self.view_profile_xpath)))

    def click_view_profile(self):
        robust_click(self, (By.XPATH, self.view_profile_xpath)).click()
        self._wait(20).until(EC.url_contains("/in/"))
        time.sleep(2)

    # ── Intro / headline ──────────────────────────────────────────────────────

    def click_edit_pencil_icon(self):
        robust_click(self, (By.XPATH, self.edit_pencil_icon_xpath)).click()
        self._wait().until(EC.visibility_of_element_located((By.XPATH, self.headline_textbox_xpath)))

    def update_headline(self, new_headline: str):
        self._clear_and_type(self.headline_textbox_xpath, new_headline)

    def update_industry(self, new_industry: str):
        self._clear_and_type(self.industry_textbox_xpath, new_industry)

    def click_save_button(self):
        robust_click(self, (By.XPATH, self.save_button_xpath)).click()
        time.sleep(2)
        # Dismiss the dialog in case it is still open after saving
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1)
        except Exception:
            pass

    # ── About ─────────────────────────────────────────────────────────────────

    def update_about(self, text: str):
        """Navigate directly to the About/summary form, use LLM-extracted XPaths to fill and save."""
        from selenium_pytest.model.profile_parser import extract_about_xpaths

        # Derive about URL from current profile URL
        current = self.driver.current_url
        if "/in/" in current:
            slug = current.split("/in/")[1].rstrip("/").split("/")[0]
            about_url = f"https://www.linkedin.com/in/{slug}/edit/forms/summary/new/"
        else:
            about_url = "https://www.linkedin.com/in/me/edit/forms/summary/new/"

        self.driver.get(about_url)
        time.sleep(3)

        # Save page HTML
        html = self.driver.page_source
        os.makedirs(_SYSTEM_DIR, exist_ok=True)
        with open(_ABOUT_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        # Use cached XPaths if available, otherwise ask LLM
        if os.path.exists(_ABOUT_XPATH_CACHE):
            with open(_ABOUT_XPATH_CACHE, "r") as f:
                xpaths = json.load(f)
        else:
            xpaths = extract_about_xpaths(html)
            with open(_ABOUT_XPATH_CACHE, "w") as f:
                json.dump(xpaths, f, indent=2)

        # Fill the textbox — tiptap renders a contenteditable div inside the wrapper
        textbox_xpath = xpaths.get("about_textbox")
        if textbox_xpath:
            # Wait for wrapper, then target the inner contenteditable div
            self._wait().until(EC.presence_of_element_located((By.XPATH, textbox_xpath)))
            editable_xpath = textbox_xpath + "//div[@contenteditable='true']"
            editable = self._wait().until(EC.presence_of_element_located((By.XPATH, editable_xpath)))
            self.driver.execute_script("arguments[0].focus();", editable)
            time.sleep(0.5)
            editable.send_keys(Keys.CONTROL + "a")
            editable.send_keys(text)
            time.sleep(1)

        # Save
        save_xpath = xpaths.get("save_button")
        if save_xpath:
            robust_click(self, (By.XPATH, save_xpath)).click()
            time.sleep(2)

        self.go_to_profile()

    # ── Education ─────────────────────────────────────────────────────────────

    def add_education(self, school: str, degree: str, field: str, start: str, end: str):
        """Navigate to the education add page, download HTML, ask LLM for XPaths, fill and save."""
        from selenium_pytest.model.profile_parser import extract_education_xpaths

        # Derive education add URL from current profile URL
        current = self.driver.current_url
        if "/in/" in current:
            slug = current.split("/in/")[1].rstrip("/").split("/")[0]
            edu_url = f"https://www.linkedin.com/in/{slug}/edit/forms/education/new/"
        else:
            edu_url = "https://www.linkedin.com/in/me/edit/forms/education/new/"

        self.driver.get(edu_url)
        time.sleep(3)

        # Save page HTML to system folder
        html = self.driver.page_source
        os.makedirs(_SYSTEM_DIR, exist_ok=True)
        with open(_EDU_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        # Use cached XPaths if available, otherwise ask LLM
        if os.path.exists(_EDU_XPATH_CACHE):
            with open(_EDU_XPATH_CACHE, "r") as f:
                xpaths = json.load(f)
        else:
            xpaths = extract_education_xpaths(html)
            with open(_EDU_XPATH_CACHE, "w") as f:
                json.dump(xpaths, f, indent=2)

        # Fill form fields using JS click to bypass any overlapping dialogs/dropdowns
        def _js_type(xpath, text):
            el = self._wait().until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(0.3)
            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.DELETE)
            el.send_keys(text)
            time.sleep(1)
            # Dismiss typeahead suggestion dropdown
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)

        if school and xpaths.get("school"):
            _js_type(xpaths["school"], school)
        if degree and xpaths.get("degree"):
            _js_type(xpaths["degree"], degree)
        if field and xpaths.get("field"):
            _js_type(xpaths["field"], field)
        if start and xpaths.get("start_year"):
            self._clear_and_type(xpaths["start_year"], start)
            time.sleep(0.5)
        if end and xpaths.get("end_year"):
            self._clear_and_type(xpaths["end_year"], end)
            time.sleep(0.5)

        if xpaths.get("save_button"):
            robust_click(self, (By.XPATH, xpaths["save_button"])).click()
            time.sleep(2)

    # ── Skills ────────────────────────────────────────────────────────────────

    def add_skill(self, skill_name: str):
        """Open the skill form from profile, type the skill name, and save."""
        if ":" in skill_name:
            skill_name = skill_name.split(":")[0].strip()

        self.go_to_profile()

        opened = False
        for xpath in (
            "//button[contains(@aria-label,'Add skill')]",
            "//a[contains(@aria-label,'Add skill')]",
            "//button[contains(@aria-label,'Add skills')]",
        ):
            try:
                btn = self._wait(5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                btn.click()
                opened = True
                time.sleep(1)
                break
            except Exception:
                continue

        if not opened:
            for xpath in (
                "//button[contains(@aria-label,'Add profile section')]",
                "//button[contains(.,'Add profile section')]",
                self.add_section_button_xpath,
            ):
                try:
                    section_btn = robust_click(self, (By.XPATH, xpath))
                    section_btn.click()
                    time.sleep(1)
                    break
                except Exception:
                    continue
            else:
                raise RuntimeError("Could not open Add profile section menu")

            for xpath in (
                "//span[normalize-space()='Add skills']/ancestor::button[1]",
                "//div[normalize-space()='Add skills']",
                "//button[contains(.,'Add skills')]",
            ):
                try:
                    skill_option = robust_click(self, (By.XPATH, xpath))
                    skill_option.click()
                    time.sleep(1)
                    break
                except Exception:
                    continue
            else:
                raise RuntimeError("Could not select Add skills from section menu")

        typed = False
        for xpath in (
            self.skill_name_xpath,
            "//input[contains(@placeholder,'Skill')]",
            "//input[contains(@aria-label,'Skill')]",
        ):
            try:
                self._clear_and_type(xpath, skill_name)
                typed = True
                break
            except Exception:
                continue
        if not typed:
            raise RuntimeError(f"Could not enter skill: {skill_name}")

        time.sleep(0.5)
        for xpath in (
            self.skill_save_xpath,
            "//button[normalize-space()='Save']",
        ):
            try:
                robust_click(self, (By.XPATH, xpath)).click()
                time.sleep(1.5)
                return
            except Exception:
                continue
        raise RuntimeError(f"Could not save skill: {skill_name}")

    # ── Projects ──────────────────────────────────────────────────────────────

    def add_project(self, name: str, description: str, url: str):
        """Open the project form from profile, fill fields, and save."""
        self.go_to_profile()

        opened = False
        for xpath in (
            "//button[contains(@aria-label,'Add project')]",
            "//a[contains(@aria-label,'Add project')]",
        ):
            try:
                btn = self._wait(5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                btn.click()
                opened = True
                time.sleep(1)
                break
            except Exception:
                continue

        if not opened:
            section_btn = robust_click(
                self,
                (
                    By.XPATH,
                    "//button[contains(.,'Add profile section') or contains(.,'Add section')]",
                ),
            )
            section_btn.click()
            time.sleep(1)
            project_option = robust_click(
                self,
                (
                    By.XPATH,
                    "//span[normalize-space()='Add projects']/ancestor::button[1]"
                    " | //div[normalize-space()='Add projects']",
                ),
            )
            project_option.click()
            time.sleep(1)

        self._clear_and_type(self.project_name_xpath, name)
        time.sleep(0.5)

        if description:
            self._clear_and_type(self.project_desc_xpath, description)
            time.sleep(0.5)

        if url:
            self._clear_and_type(self.project_url_xpath, url)
            time.sleep(0.5)

        robust_click(self, (By.XPATH, self.project_save_xpath)).click()
        time.sleep(2)
