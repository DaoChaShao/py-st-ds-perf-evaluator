#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/22 20:55
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   home.py
# @Desc     :   

from streamlit import title, divider, expander, caption, empty

title("DeepSeek Evaluator")
divider()
with expander("Introduction", expanded=True):
    caption("This is a **utilis** that can give a evaluation to a student.")
    caption("1. Select the LLM model you want to use.")
    caption("2. Select the temperature of the LLM model.")
    caption("3. Upload a PDF file of a student's performance.")
    caption("4. ~~Select the embedding model you want to use.~~")
    caption("5. The utilis will give a creative evaluation of the performance.")
    caption("6. The utilis will provide some suggestions for improvement.")

empty_message = empty()
