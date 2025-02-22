#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/22 20:56
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   layout.py
# @Desc     :   

from streamlit import Page, navigation


def pages_setter() -> None:
    """ Set the subpages on the sidebar """
    pages: dict = {
        "page": [
            "subpages/home.py",
            "subpages/deepseek.py",
        ],
        "title": [
            "Home",
            "Evaluation",
        ],
        "icon": [
            ":material/home:",
            ":material/calculate:",
        ],
    }

    structure: dict = {
        "Introduction": [
            Page(page=pages["page"][0], title=pages["title"][0], icon=pages["icon"][0]),
        ],
        "DeepSeek Model": [
            Page(page=pages["page"][1], title=pages["title"][1], icon=pages["icon"][1]),
        ]
    }
    pg = navigation(structure, position="sidebar", expanded=True)
    pg.run()
