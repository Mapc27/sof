function add_comment(element, discussion = false, answer_id = null) {
    $(document).ready(function () {
        let text;
        let url;
        text = element.previousElementSibling.value
        if (discussion === true) {
            url = window.location.href + "/new_comment";
        } else {
            url = window.location.href + "/answer/" + answer_id + "/new_comment";
        }

        let data = {
            'text': text,
        }

        $.ajax({
            url: url,
            type: "POST",
            data: data,
            success: function (response_dict) {
                console.log(response_dict)
                let commentary_id = response_dict['commentary_id']
                let commentary_text = response_dict['commentary_text']
                let commentary_grade = response_dict['commentary_grade']
                let commentary_updated_at = response_dict['commentary_updated_at']
                let commentary_user = response_dict['commentary_user']

                let html_text =
                    `<tr class="commentary-row">
                    <td class="commentary-data">

                    </td>
                    <td class="commentary-data">

                        <div class="commentary">
                            <div class="commentary-text">
                                ${commentary_text} –
                                <a href="${commentary_user['href']}" class="commentary-user-link user-link">${commentary_user['nickname']}</a>
                                ${commentary_updated_at}
                            </div>
                        </div>
                    </td>
               </tr>`

                let last_commentary = $(element).closest('.new_commentary-row')[0]
                if (last_commentary === undefined || last_commentary.previousElementSibling === null) {
                    last_commentary = $(element).closest("tbody")[0]
                    console.log(last_commentary)
                    last_commentary.innerHTML = html_text + last_commentary.innerHTML
                }
                else { last_commentary.previousElementSibling.outerHTML += html_text }

                element.previousElementSibling.value = ''
            }
        });
    }
    );
}

function add_answer() {
    $(document).ready(function () {
        let text = $("#new_answer-text")[0];

        let data = {
            'text': text.value,
        }

        let url = window.location.href + '/new_answer'
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            success: function (response_dict) {
                let answer_id = response_dict['answer_id'];
                let answer_grade = response_dict['answer_grade'];
                let answer_text = response_dict['answer_text']
                let answer_updated_at = response_dict['answer_updated_at']
                let answer_user = response_dict['answer_user']

                let question_answer = document.getElementsByClassName("question_answer")[1].getElementsByTagName('tbody')[0]
                question_answer.innerHTML +=
                    `<tr class="question_answer-row">
                            <td class="question_answer-data">
                            <svg aria-hidden="true" class="svg-icon iconArrowUpLg" width="36" height="36" viewBox="0 0 36 36" onclick="change_grade(element=this, discussion=false, answer=true, discussion_id='{{discussion.id}}', answer_id=${answer_id} , up=true)">
                                <path class="change_grade" d="M2 26h32L18 10 2 26Z"></path>
                            </svg>

                            <div class="question_answer-grade">${answer_grade}</div>

                            <svg aria-hidden="true" class="svg-icon iconArrowDownLg" width="36" height="36" viewBox="0 0 36 36" onclick="change_grade(element=this, discussion=false, answer=true, discussion_id='{{discussion.id}}', answer_id=${answer_id}, up=false)">
                                <path class="change_grade" d="M2 10h32L18 26 2 10Z"></path>
                            </svg>

                        </td>
                            <td class="question_answer-data">
                                <div class="question_answer-text">
                                    ${answer_text}
                                </div>
                                <div class="question_answer-author_data">
                                    <div class="question_answer-user">
                                        <a href="${answer_user['href']}" class="question_answer-user-link user-link">${answer_user['nickname']}</a>
                                    </div>
                                    <div class="question_answer-datetime datetime">${answer_updated_at}</div>
                                </div>
                                <table class="commentaries">
                                        <tr class="new_commentary-row">
                                            <td></td>
                                            <td class="new_commentary-data">
                                                <div class="input-group mb-3">
                                                    <input id="${answer_id}" type="text" class="form-control answer_commentary_input" placeholder="Add a new comment">
                                                    <button class="btn btn-outline-secondary" type="button" onclick="add_comment(element=this, discussion=false, answer_id='${answer_id}')">Add</button>
                                                </div>
                                            </td>
                                        </tr>
                                </table>
                            </td>
                        </tr>`
                let under_question = document.getElementsByClassName("under_question")[0].getElementsByTagName('span')[0]
                under_question.innerHTML = Number(under_question.innerHTML) + 1
                text.value = ''
            }
        });
    }
    );
}

function change_grade(element, discussion = false, answer_id = null, up = false) {
    arrow = element.getElementsByClassName("change_grade")[0]

    if (arrow.classList.contains("pressed")){
        arrow.classList.remove("pressed")
    }

    else {
        other_arrow = element.parentNode.getElementsByClassName("change_grade")
        if (other_arrow[0] === arrow){
            other_arrow = other_arrow[1]
        }
        else{
            other_arrow = other_arrow[0]
        }

        if (other_arrow.classList.contains("pressed")){
            other_arrow.classList.remove("pressed")
        }
    }
    

    let url;
    if (discussion === true) {
        url = window.location.href + '/change_grade'
    }
    else {
        url = window.location.href + '/answer/' + answer_id + '/change_grade'
    }

    data = {
        "up": up,
    }

    $.ajax({
        url: url,
        type: "POST",
        data: data,
        success: function (response_dict) {
            arrow.classList.add("pressed")
            grade = response_dict['grade']
            if (grade != null){
                element.parentNode.getElementsByClassName("question_answer-grade")[0].innerHTML = grade
            }
        }
    });
}
