#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/22 20:55
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   deepseek.py
# @Desc     :   

from pandas import DataFrame
from streamlit import empty, data_editor, spinner, markdown, sidebar

from utilis.tools import (hyperparams_getter, file_loader, name_getter,
                          Timer, performance_analyzer, deepseek_api_model)

empty_message = empty()

params_llm: dict = hyperparams_getter(empty_message)

match len(params_llm):
    case 4:
        data_editor(DataFrame([params_llm]), hide_index=True, disabled=True, use_container_width=True)

        with spinner("Loading the file...", show_time=True):
            content = file_loader()

        if content:
            name = name_getter(content)
            if name:
                empty_message.info("Click the button to generate an evaluation.")

                if sidebar.button("Generate Evaluation", type="primary"):
                    with spinner("Generating an evaluation...", show_time=True):
                        with Timer("LLM Evaluation") as timer:
                            prompt: str = performance_analyzer(name, params_llm, content)
                            respond: str = deepseek_api_model(params_llm, prompt)
                        markdown(respond)
                        empty_message.success(f"Generating an evaluation for {name} consumes {timer} seconds.")
            else:
                empty_message.error("The name of the student is not found.")
        else:
            empty_message.error("Please upload a file with the correct format.")
    case _:
        default = {"model": [], "api_key": [], "temperature": [], "sys_content": []}
        data_editor(DataFrame(default), hide_index=True, disabled=True, use_container_width=True)
