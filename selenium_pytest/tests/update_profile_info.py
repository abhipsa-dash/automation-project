"""
update_profile_info.py

Reads user.md via the Groq LLM, extracts structured profile data,
then uses Selenium to update LinkedIn's title, about, education, skills,
and projects sections.

Before running:
  1. Fill in data/selpy_app/input/user.md with your profile details.
  2. Set GROQ_API_KEY in data/selpy_app/input/.env
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from selenium_pytest.utils.services import signIn, logout
from selenium_pytest.utils.logger import AppLogger
from selenium_pytest.utils.execution_data import record_execution, get_failure_type
from selenium_pytest.pages.profilePage import ProfilePage
from selenium_pytest.model.profile_parser import parse_profile


def update_profile(driver, logger, profile: dict):
    """Fill all LinkedIn profile sections from the parsed profile dict."""
    start = time.time()
    page = ProfilePage(driver)

    try:
        # ── Navigate to profile ────────────────────────────────────────────
        logger.info("Navigating to profile page")
        page.click_menu_icon()
        page.click_view_profile()

        # ── Title / Headline ───────────────────────────────────────────────
        if profile.get("title"):
            logger.info(f"Updating headline: {profile['title']}")
            page.click_edit_pencil_icon()
            page.update_headline(profile["title"])
            page.click_save_button()
            logger.info("Headline updated")

        # ── About ─────────────────────────────────────────────────────────
        if profile.get("about"):
            logger.info("Updating About section")
            page.update_about(profile["about"])
            logger.info("About updated")


        # ── Education ─────────────────────────────────────────────────────
        # for edu in profile.get("education", []):
        #     logger.info(f"Adding education: {edu.get('school')}")
        #     page.add_education(
        #         school=edu.get("school", ""),
        #         degree=edu.get("degree", ""),
        #         field=edu.get("field", ""),
        #         start=edu.get("start", ""),
        #         end=edu.get("end", ""),
        #     )
        #     logger.info(f"Education added: {edu.get('school')}")

        # ── Skills ────────────────────────────────────────────────────────
        # for skill in profile.get("skills", []):
        #     logger.info(f"Adding skill: {skill}")
        #     page.add_skill(skill)
        #     logger.info(f"Skill added: {skill}")

        # ── Projects ──────────────────────────────────────────────────────
        # for project in profile.get("projects", []):
        #     logger.info(f"Adding project: {project.get('name')}")
        #     page.add_project(
        #         name=project.get("name", ""),
        #         description=project.get("description", ""),
        #         url=project.get("url", ""),
        #     )
        #     logger.info(f"Project added: {project.get('name')}")

        record_execution(
            test_name="update_profile_info",
            status="passed",
            execution_time=time.time() - start,
        )
        logger.info("Profile update complete")

    except Exception as e:
        failure_type = get_failure_type(e)
        logger.error(f"update_profile_info failed: {e}")
        record_execution(
            test_name="update_profile_info",
            status="failed",
            execution_time=time.time() - start,
            failure_type=failure_type,
        )
        raise


if __name__ == "__main__":
    logger = AppLogger("update_profile_info").get_logger()

    # Step 1: Parse user.md with the LLM
    logger.info("Parsing user.md with Groq LLM...")
    profile = parse_profile()
    logger.info(f"Parsed profile — title: '{profile['title']}', "
                f"skills: {profile['skills']}, "
                f"education entries: {len(profile['education'])}, "
                f"projects: {len(profile['projects'])}")

    # Step 2: Sign in
    driver = signIn(logger)
    time.sleep(3)

    try:
        # Step 3: Update the profile
        update_profile(driver, logger, profile)
        time.sleep(3)
    finally:
        # Navigate to feed to clear any open edit dialogs, then log out
        try:
            driver.get("https://www.linkedin.com/feed/")
            time.sleep(2)
        except Exception:
            pass
        logout(driver, logger)
        driver.quit()
