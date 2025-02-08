from pandas import DataFrame
from streamlit import (title, divider, expander, caption, empty,
                       write, data_editor, spinner)

from utils import (sidebar_params_llm_getter,
                   file_loader,
                   name_getter,
                   performance_analyzer_online,
                   llm_online_getter,
                   Timer)


def main() -> None:
    """ streamlit run evaluator/main.py """
    title("DeepSeek Evaluator")
    divider()
    with expander("Introduction"):
        caption("This is a **evaluator** that can give a evaluation to a student.")
        caption("1. Select the LLM model you want to use.")
        caption("2. Select the temperature of the LLM model.")
        caption("3. Upload a PDF file of a student's performance.")
        caption("4. ~~Select the embedding model you want to use.~~")
        caption("The evaluator will give a creative evaluation of the performance.")
        caption("The evaluator will provide some suggestions for improvement.")

    empty_message = empty()

    params_llm: dict = sidebar_params_llm_getter(empty_message)
    # write(params_llm)
    match len(params_llm):
        case 4:
            data_editor(DataFrame([params_llm]), hide_index=True, disabled=True, use_container_width=True)
            content = file_loader()
            with spinner("Generating an evaluation..."):
                if content:
                    name = name_getter(content)
                    # write(content)
                    if name:
                        # write(name)
                        with Timer(precision=2) as timer:
                            prompt: str = performance_analyzer_dynamic(name, params_llm, content)
                            # write(prompt)
                            respond: str = llm_dynamic_getter(params_llm, prompt)
                        write(respond)
                        empty_message.success(f"Generating an evaluation for {name} consumes {timer} seconds.")
        case _:
            default = {"model": [], "api_key": [], "temperature": [], "sys_content": []}
            data_editor(DataFrame(default), hide_index=True, disabled=True, use_container_width=True)


if __name__ == "__main__":
    main()
