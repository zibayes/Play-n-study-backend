    let bg = document.querySelector('.mouse-parallax-bg');
    window.addEventListener('mousemove', function(e) {
        let x = e.clientX / window.innerWidth;
        let y = e.clientY / window.innerHeight;
        bg.style.transform = 'translate(-' + x * 150 + 'px, -' + y * 150 + 'px)';
    });

    function update(chat_id, date_message) {

    }



    let div_main = document.getElementsByClassName('chats')[0]

    $.ajax({
      url: '/get_chats',
      method: 'post',
      dataType: 'json',
      success: function(json_data){
        console.log(json_data)
        json_data.chats.sort(
                function (a, b){
                  return new Date(b.time) - new Date(a.time)
                }
        )
        for (let i = 0; i < json_data.chats.length; i++){
          let div = add_element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id)
          div_main.appendChild(div)
        }
      }
    });



  function add_element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id) {
    // 1 +
    let div_add = document.createElement("div")
    div_add.setAttribute("class", "collapse mt-3")
    div_add.id = "collapse" + chat_id
    // 2 +
    let div_card = document.createElement("div")
    div_card.setAttribute("class", "card")
    // 3 +
    let button_exit = document.createElement("button")
    button_exit.setAttribute("class", "btn-close")
    button_exit.setAttribute("type", "button")
    button_exit.setAttribute("data-mdb-toggle", "collapse")
    let href = "#collapse" + chat_id
    button_exit.setAttribute("href", href)
    button_exit.style = "padding: 10px"
    // 4
    let div_card_body = document.createElement("div")
    div_card_body.setAttribute("class", "card-body")
    div_card_body.setAttribute("data-mdb-perfect-scrollbar", "true")
    div_card_body.style = "position: relative; height: 400px; overflow: auto;"
    div_card_body.id = "div" + chat_id
    // 5
    // Элементы чата тут будут
    let date_message
    $.ajax({
              url: '/get_dialog',
              method: 'post',
              dataType: 'json',
              contentType: 'application/json',
              data: JSON.stringify({"chat_id": chat_id}),
              success: function (data) {
                date_message = data.messages[data.messages.length - 1].msg_date
                for (let i = 0; i < data.messages.length; i++) {
                  if (data.messages[i].msg_from === "Я: ") {
                    let div_element_d_flex = document.createElement("div")
                    div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
                    let div_element = document.createElement("div")
                    let flag = 0
                    for (let j = i; j < data.messages.length; j++) {
                      flag++
                      if (data.messages[j].msg_from === "Я: ") {
                        let p1 = document.createElement("p")
                        p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
                        p1.textContent = data.messages[j].msg_text
                        div_element.appendChild(p1)
                      } else {
                        i = i + flag - 2
                        break
                      }
                      if (j === data.messages.length - 1) {
                        i = data.messages.length
                        break
                      }
                    }
                    let image = document.createElement("img")
                    image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
                    image.alt = ""
                    image.style = "width: 45px; height: 100%;"
                    div_element_d_flex.appendChild(div_element)
                    div_element_d_flex.appendChild(image)
                    div_card_body.appendChild(div_element_d_flex)
                  } else {
                    let div_element_d_flex = document.createElement("div")
                    div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-start")
                    let image = document.createElement("img")
                    image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
                    image.alt = ""
                    image.style = "width: 45px; height: 100%;"
                    let div_element = document.createElement("div")
                    let flag = 0
                    for (let j = i; j < data.messages.length; j++) {
                      flag++
                      if (data.messages[j].msg_from !== "Я: ") {
                        let p1 = document.createElement("p")
                        p1.setAttribute("class", "small p-2 ms-3 mb-1 rounded-3")
                        p1.style = "background-color: #f5f6f7;"
                        p1.textContent = data.messages[j].msg_text
                        div_element.appendChild(p1)
                      } else {
                        i = i + flag - 2
                        break
                      }
                      if (j === data.messages.length - 1) {
                        i = data.messages.length
                        break
                      }
                    }
                    div_element_d_flex.appendChild(image)
                    div_element_d_flex.appendChild(div_element)
                    div_card_body.appendChild(div_element_d_flex)

                  }
                }
              }
            }
    );


    // 6
    let div_container = document.createElement("div")
    div_container.setAttribute("class", "container")
    // 7
    let div_row = document.createElement("div")
    div_row.setAttribute("class", "row card-footer text-muted align-items-center")
    // 8
    let div_column1 = document.createElement("div")
    div_column1.setAttribute("class", "col-md-10")
    // 9
    let textarea = document.createElement("textarea")
    textarea.id = "textarea" + chat_id
    textarea.setAttribute("class", "shoutbox-name form-control form-control-lg")
    textarea.setAttribute("type", "text")
    textarea.setAttribute("placeholder", "Введите сообщение")
    // 10
    let div_column2 = document.createElement("div")
    div_column2.setAttribute("class", "col-md-1")
    div_column2.style = "padding: 0 0 0 10px"
    // 11
    let a1 = document.createElement("a")
    a1.setAttribute("class", "ms-1 text-muted")
    a1.setAttribute("href", "#!")
    // 12
    let i1 = document.createElement("i")
    i1.setAttribute("class", "fas fa-paperclip")
    // 13
    let div_column3 = document.createElement("div")
    div_column3.setAttribute("class", "col-md-1")
    // 14
    let a2 = document.createElement("a")
    a2.setAttribute("class", "ms-3 link-info")
    a2.setAttribute("href", "#!")
    a2.addEventListener("click", function () {
      var input = document.getElementById("textarea" + chat_id)
      if (input.value !== ""){
        $.ajax({
          url: '/send_message',
          method: 'post',
          dataType: 'html',
          contentType:'application/json',
          data: JSON.stringify({"msg_text": input.value, "msg_to": user_with_id}),
          success: function(data){
            input.value = ""
          }
        });
      }
    })
    setInterval(function () {
      $.ajax({
        url: '/get_dialog',
        method: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"chat_id": chat_id}),
        success: function (data) {
          if(new Date(data.messages[data.messages.length - 1].msg_date) > new Date(date_message)){
              // Собеседник
              var div_card_element = document.getElementById("div" + chat_id)
              let div_element_d_flex = document.createElement("div")
              div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
              let div_element = document.createElement("div")
              let image = document.createElement("img")
              image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
              image.alt = ""
              image.style = "width: 45px; height: 100%;"
              let p1 = document.createElement("p")
              p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
              p1.textContent = data.messages[data.messages.length - 1].msg_text
              div_element.appendChild(p1)
              div_element_d_flex.appendChild(div_element)
              div_element_d_flex.appendChild(image)
              div_card_element.appendChild(div_element_d_flex)
              date_message = data.messages[data.messages.length - 1].msg_date
          }
        }
      })
      console.log(date_message)
    }, 500)
    // 15
    let i2 = document.createElement("i")
    i2.setAttribute("class", "fas fa-paper-plane")
    // Соединяем элементы
    a2.appendChild(i2)
    div_column3.appendChild(a2)
    a1.appendChild(i1)
    div_column2.appendChild(a1)
    div_column1.appendChild(textarea)
    div_row.appendChild(div_column1)
    div_row.appendChild(div_column2)
    div_row.appendChild(div_column3)
    div_container.appendChild(div_row)
    div_card.appendChild(button_exit)
    div_card.appendChild(div_card_body)
    div_card.appendChild(div_container)
    div_add.appendChild(div_card) // !
    // 16!
    let br = document.createElement("br")
    // 17
    let a = document.createElement("a")

    a.setAttribute("data-mdb-toggle", "collapse")
    a.setAttribute("href", href)
    a.setAttribute("role", "button")
    a.setAttribute("aria-expanded", "false")
    // 18
    let div_card_body2 = document.createElement("div")
    div_card_body2.setAttribute("class", "card-body")
    // 19
    let div_card_pos = document.createElement("div")
    div_card_pos.setAttribute("class", "position-relative position-relative-example")
    // 20
    let div_card_pos_1 = document.createElement("div")
    div_card_pos_1.setAttribute("class", "position-absolute top-0 end-0 text-muted")
    let time_correct = new Date(time)
    let today = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(time_correct);
    let seconds = ""
    if (time_correct.getSeconds() < 10){
      seconds = "0" + time_correct.getSeconds()
    }
    else{
      seconds = time_correct.getSeconds()
    }
    div_card_pos_1.textContent = today + " " + time_correct.getHours() + ":" + seconds
    div_card_pos_1.style = "font-size: 75%"
    // 21 Уведомление!
    let div_card_pos_2 = document.createElement("div")
    if (checked === true){
      a.setAttribute("class", "card elements opacity-75")
    }else{
      a.setAttribute("class", "card elements")
      div_card_pos_2.setAttribute("class", "position-absolute top-0 start-50 text-warning")
      div_card_pos_2.textContent = "Уведомление!"
      div_card_pos_2.style = "font-size: 75%"
    }
    // 22
    let div_container2 = document.createElement("div")
    div_container2.setAttribute("class", "container")
    // 23
    let div_row2 = document.createElement("div")
    div_row2.setAttribute("class", "row")
    // 24
    let div_col1 = document.createElement("div")
    div_col1.setAttribute("class", "col-md-2")
    div_col1.style = "padding: 10px 0 10px 0"
    // 25
    let img = document.createElement("img")
    img.setAttribute("src", "https://blog.getbootstrap.com/assets/img/2022/05/docs-home.png")
    img.setAttribute("alt", "")
    img.setAttribute("class", "rounded-circle")
    img.style = "width: 45px; height: 45px"
    // 26
    let div_col2 = document.createElement("div")
    div_col2.setAttribute("class", "col-md-10")
    div_col2.style = "padding: 10px 0 0 10px"
    // 27
    let p1 = document.createElement("p")
    p1.setAttribute("class", "fw-bold mb-1 lang text-muted")
    p1.textContent = user_with
    // 28
    let div_flex = document.createElement("div")
    div_flex.setAttribute("class", "d-flex")
    // 29
    let span = document.createElement("div")
    span.setAttribute("class", "text-muted lang fw-bold")
    span.style = "font-size: 75%"
    span.textContent = from_who + ":"
    // 30
    let p2 = document.createElement("p")
    p2.setAttribute("class", "lang text-muted text-truncate")
    p2.style = "font-size: 75%"
    p2.textContent = last_message
    // Соединяем
    div_col2.appendChild(p1)
    div_flex.appendChild(span)
    div_flex.appendChild(p2)
    div_col2.appendChild(div_flex)
    div_col1.appendChild(img)
    div_row2.appendChild(div_col1)
    div_row2.appendChild(div_col2)
    div_container2.appendChild(div_row2)
    div_card_pos.appendChild(div_card_pos_1)
    div_card_pos.appendChild(div_card_pos_2)
    div_card_body2.appendChild(div_card_pos)
    div_card_body2.appendChild(div_container2)
    a.appendChild(div_card_body2) // !
    let div_main = document.createElement("div")
    div_main.appendChild(div_add)
    div_main.appendChild(br)
    div_main.appendChild(a)
    return div_main
  }

    $('.shoutbox-name').emojioneArea({
      emojiPlaceholder: ":smile_cat:",
      searchPlaceholder: "Поиск",
      buttonTitle: "Эмодзи",
      searchPosition: "top",
      pickerPosition: "top"
    });

var arrLang = {
  'en': {
    'mainpage': 'Main page',
    'support': 'Support',
    'profile': 'Profile',
    'my_profile': 'My profile',
    'my_friends': 'My subscriptions',
    'my_subscriptions': 'My courses',
    'my_achievements': 'My achievements',
    'achievements': 'Achievements',
    'timetable': 'My timetable',
    'settings': 'Settings',
    'reviews': 'Reviews',
    'aboutus': 'About us',
    'exit': 'Logout',
    'areusure': 'Are you sure you want to log out?',
    'confirmexit': 'Confirm logout',
    'logout': 'Log out of your account',
    'flag': 'flag-united-kingdom',
    'your_chats': 'Your chats',
    'admin': 'ADMINISTRATOR',
    'subscribe': 'Subscribe',
    'unsubscribe': 'Unsubscribe',
    'give_admin': 'Grant administrator permissions',
    'remove_admin': 'Depose administrator permissions',
    'info': 'More information',
    'subscriptions': 'Subscriptions',
    'subscriptions_': 'subscriptions',
    'subscribers': 'subscribers',
    'participant_in': 'Participant in',
    'founded_by_request': 'Found on request:',

    'users_courses': 'User\'s courses',
    'create_course': 'Create course',
    'course_creation': 'Course creation',
    'enter_course_data': 'Enter course data:',
    'create': 'Create',

    'createform': 'Create form',
    'form': 'Form',

    'maininfo': 'Main information',
    'changeava': 'Change avatar',
    'anachievements': 'Achievements',
    'name': 'Name',
    'surname': 'Surname',
    'phonenumber': 'Phone number',
    'email': 'Email',
    'city': 'City:',
    'city_': 'City',
    'university': 'University',
    'specialization': 'Specialization',
    'group': 'Group',
    'save': 'Save',

    'devteam': 'Development team',
    'pavel': 'Pavel',
    'pavinfo': 'Backend and frontend developer',
    'online': 'Online',
    'ilya': 'Ilya',
    'ilyinfo': 'Frontend developer',
    'offline': 'Offline',
    'anton': 'Anton',
    'antinfo': 'Backend developer',
    'afk': 'AFK',
    'devinfo': 'Information about developer',

    'my_notes': 'My notes',
    'my_tasks': 'My tasks',
    'month': 'Month',

    "monday": "MO",
    "tuesday": "TU",
    "wednesday": "WE",
    "thursday": "TH",
    "friday": "FR",
    "saturday": "SA",
    "sunday": "SU",

    "course": "Course",
    "courses": "Courses",
    "course_rating": "Course rating:",
    "rate_first": "This course has not been rated yet, be the first!",
    "go_to_course": "Go to the course",
    "edit_course": "Edit course",
    "delete_course": "Delete course",
    "course_participants": "Course participants",
    "desc": "Description",
    "thanks_for_your_feedback": "Thanks for the feedback!",
    "how_do_you_like_this_course": "How do you like this course?",
    "give_us_feedback": "Leave your feedback:",
    "what_about_comment": "What about the comment?",
    "course_participants_feedback": "Feedback from course participants",
    "feedback_without_comment": "--- Review without comment ---",
    "show_all_feedback": "View all course reviews",
    "confirm_delete_course": "Confirmation of course deletion",
    "are_u_sure_delete_course": "Are you sure you want to delete the course",
    "delete": "Delete",

    "course_participants_of": "Participants of the course",
    "curator": "CURATOR",
    "give_curator": "Grant curator permissions",
    "remove_curator": "Depose curator permissions",

    "course_content": "Course content",
    "test": "Test",
    "article": "Article",
    "done": "Done",
    "checking": "On checking",
    "not_done": "Not done",
    "show_summary": "View progress summary",
    "test_desc": "Answer the questions and get a prize",
    "article_desc": "Read the article and eat a candy",

    "course_summary": "Course summary",
    "course_unit": "Course task",
    "tesk_type": "Type",
    "status": "Status",
    "mark": "Mark",
    "unit": "Unit",
    "result": "Result",
    "unit_result": "Result of unit",

    "read_article": "The article was read",

    "show_tries": "Viewing tries",
    "leaders_table": "Leaderboard",
    "progress_graphic": "Progress graphic",
    "friends_progress": "Friends\' Progress",
    "last_tries": "The results of your previous tries",
    "try_number": "Try number",
    "condition": "Condition",
    "viewing": "Viewing",
    "time_spent": "Time spent on passing",
    "show_try": "View try",
    "best_mark": "Best mark:",
    "best_mark_": "Best mark",
    "place": "Place",
    "user": "User",
    "graphic_desc": "The graphic of the distribution of users according to the best mark",
    "friends_table_desc": "Leaderboard among friends you are subscribed to",
    "marking_method": "Assessment method: Teacher",
    "start_test": "Start test",

    "try_showing": "Viewing try",
    "information": "Information",
    "question": "Question",
    "score": "Score:",
    "not_marked": "Not marked",
    "the_same_answer": "users gave the same answer to this task",
    "curator_comment": "Curator\'s comment:",
    "your_result": "Your result:",
    "your_time_spent": "Time passed ",

    "passing_the_test": "Passing the test",
    "complete_test": "Complete the test",

    "course_reviews": "Reviews of the course",

    "course_editing": "Editing the course",
    "check": "Checking",
    "edit": "Edit",
    "task_creation": "Creating a task",
    "choose_task_type": "Select the type of task to be created:",
    "confirm_delete_unit": "Confirmation of deleting a unit",
    "confirm_delete_test": "Confirmation of deleting the test",
    "confirm_delete_article": "Confirmation of deleting the article",
    "are_u_sure_delete_unit": "Are you sure you want to delete the unit",
    "are_u_sure_delete_test": "Are you sure you want to delete the test",
    "are_u_sure_delete_article": "Are you sure you want to delete the article",
    "unit_creation": "Creating a unit",
    "enter_unit_name": "Enter the name of the unit:",
    "save_course": "Save course",

    "article_edit": "Article editing",
    "article_edit_of": "Editing of article",
    "enter_article": "Entering an article (in Markdown)",
    "article_text": "Article text",
    "article_preview": "Article preview",
    "save_article": "Save article",

    "article_constructor": "Article constructor",

    "test_checking": "Checking test",
    "tires_results": "Tires results",
    "check_try": "Check the try",

    "test_checking_user": "Checking the try of user",
    "add_comment": "Add comment",
    "result_": "Result:",
    "complete_checking": "Complete checking",

    "test_editor_of": "Editing of test",
    "test_editor": "Test editor",
    "solo": "Solo answer",
    "multiple": "Multiple answer",
    "free": "Free answer",
    "detailed_free": "Detailed free answer",
    "info_block": "Informational unit",
    "add_question": "Add question",
    "save_test": "Save test",
    "add_answer": "Add answer",
    "delete_answer": "Delete answer",

    "test_constructor": "Test constructor",

    "access_denied": "Access denied",
    "but_you_can_subscribe": "But you can get access to the materials of this course by subscribing to it",

    "new_note": "New note",
    "name_": "Name:",
    "note_": "Note:",
    "exit": "Exit",
  },
  'ru': {
    'mainpage': 'Главная',
    'support': 'Поддержка',
    'profile': 'Профиль',
    'my_profile': 'Мой профиль',
    'my_friends': 'Мои подписки',
    'my_subscriptions': 'Мои курсы',
    'my_achievements': 'Мои награды',
    'achievements': 'Достижения',
    'timetable': 'Мое расписание',
    'settings': 'Настройки',
    'reviews': 'Отзывы',
    'aboutus': 'О нас',
    'exit': 'Выйти',
    'areusure': 'Вы точно хотите выйти?',
    'confirmexit': 'Подтверждение выхода',
    'logout': 'Выход из учетной записи',
    'flag': 'flag-russia',
    'your_chats': 'Ваши диалоги',
    'admin': 'АДМИНИСТРАТОР',
    'subscribe': 'Подписаться',
    'unsubscribe': 'Отписаться',
    'give_admin': 'Выдать полномочия администратора',
    'remove_admin': 'Низложить полномочия администратора',
    'info': 'Подробнее',
    'subscriptions': 'Подписки',
    'subscriptions_': 'подписки',
    'subscribers': 'подписчиков',
    'participant_in': 'Участник в',
    'founded_by_request': 'Найдено по запросу:',

    'users_courses': 'Пользовательские курсы',
    'create_course': 'Создать курс',
    'course_creation': 'Создание курса',
    'enter_course_data': 'Введите данные курса:',
    'create': 'Создать',

    'createform': 'Создание формы',
    'form': 'Форма',

    'maininfo': 'Основная информация',
    'changeava': 'Сменить аватар',
    'anachievements': 'Достижения',
    'name': 'Имя',
    'surname': 'Фамилия',
    'phonenumber': 'Номер телефона',
    'email': 'Электронная почта',
    'city': 'Город:',
    'city_': 'Город',
    'university': 'Институт',
    'specialization': 'Специальность',
    'group': 'Учебная группа',
    'save': 'Сохранить',

    'devteam': 'Команда разработчиков',
    'pavel': 'Павел',
    'pavinfo': 'Бэкенд и Фронтенд разработчик',
    'online': 'На сайте',
    'ilya': 'Илья',
    'ilyinfo': 'Фронтэнд разработчик',
    'offline': 'Оффлайн',
    'anton': 'Антон',
    'antinfo': 'Бэкенд разработчик',
    'afk': 'Спит',
    'devinfo': 'Информация о разработчике',

    'my_notes': 'Мои заметки',
    'my_tasks': 'Мои задачи',
    'month': 'Месяц',

    "monday": "ПН",
    "tuesday": "ВТ",
    "wednesday": "СР",
    "thursday": "ЧТ",
    "friday": "ПТ",
    "saturday": "СБ",
    "sunday": "ВС",

    "course": "Курс",
    "courses": "Курсы",
    "course_rating": "Рейтинг курса:",
    "rate_first": "Данный курс пока не оценили, будьте первым!",
    "go_to_course": "Перейти на курс",
    "edit_course": "Редактировать курс",
    "delete_course": "Удалить курс",
    "course_participants": "Участники курса",
    "desc": "Описание",
    "thanks_for_your_feedback": "Спасибо за отзыв!",
    "how_do_you_like_this_course": "Как вам данный курс?",
    "give_us_feedback": "Оставьте свой отзыв:",
    "what_about_comment": "А как насчёт комментария?",
    "course_participants_feedback": "Отзывы участников курса",
    "feedback_without_comment": "--- Отзыв без комментария ---",
    "show_all_feedback": "Посмотреть все отзывы о курсе",
    "confirm_delete_course": "Подтверждение удаления курса",
    "are_u_sure_delete_course": "Вы точно хотите удалить курс",
    "delete": "Удалить",

    "course_participants_of": "Участники курса",
    "curator": "КУРАТОР",
    "give_curator": "Выдать полномочия куратора",
    "remove_curator": "Низложить полномочия куратора",

    "course_content": "Содержание курса",
    "test": "Тест",
    "article": "Статья",
    "done": "Выполнено",
    "checking": "На проверке",
    "not_done": "Не выполнено",
    "show_summary": "Посмотреть сводку о прогрессе",
    "test_desc": "Ответьте на вопросы и получите приз",
    "article_desc": "Прочтите статью и съешьте конфетку",

    "course_summary": "Сводка о курсе",
    "course_unit": "Элемент курса",
    "tesk_type": "Тип",
    "status": "Статус",
    "mark": "Оценка",
    "unit": "Раздел",
    "result": "Итог",
    "unit_result": "Итог раздела",

    "read_article": "Статья прочитана",

    "show_tries": "Просмотр попыток",
    "leaders_table": "Таблица лидеров",
    "progress_graphic": "График прогресса",
    "friends_progress": "Прогресс друзей",
    "last_tries": "Результаты ваших предыдущих попыток",
    "try_number": "Номер попытки",
    "condition": "Состояние",
    "viewing": "Просмотр",
    "time_spent": "Потрачено времени на прохождение",
    "show_try": "Посмотреть попытку",
    "best_mark": "Высшая оценка:",
    "best_mark_": "Высшая оценка",
    "place": "Место",
    "user": "Пользователь",
    "graphic_desc": "График распределения пользователей по высшей оценке",
    "friends_table_desc": "Таблица лидеров среди друзей, на кого вы подписаны",
    "marking_method": "Метод оценивания: Преподаватель",
    "start_test": "Начать тест",

    "try_showing": "Просмотр попытки",
    "information": "Информация",
    "question": "Вопрос",
    "score": "Баллы:",
    "not_marked": "Не оценено",
    "the_same_answer": "пользователей дали такой же ответ на данное задание",
    "curator_comment": "Комментарий куратора:",
    "your_result": "Ваш результат:",
    "your_time_spent": "Прошло времени ",

    "passing_the_test": "Прохождение теста",
    "complete_test": "Завершить тест",

    "course_reviews": "Отзывы о курсе",

    "course_editing": "Редактирование курса",
    "check": "Проверка",
    "edit": "Редактировать",
    "task_creation": "Создание задания",
    "choose_task_type": "Выберите тип создаваемого задания:",
    "confirm_delete_unit": "Подтверждение удаления раздела",
    "confirm_delete_test": "Подтверждение удаления теста",
    "confirm_delete_article": "Подтверждение удаления статьи",
    "are_u_sure_delete_unit": "Вы точно хотите удалить раздел",
    "are_u_sure_delete_test": "Вы точно хотите удалить тест",
    "are_u_sure_delete_article": "Вы точно хотите удалить статью",
    "unit_creation": "Создание раздела",
    "enter_unit_name": "Введите название раздела:",
    "save_course": "Сохранить курс",

    "article_edit": "Составление статьи",
    "enter_article": "Ввод статьи (в Markdown)",
    "article_text": "Текст статьи",
    "article_preview": "Превью вашей статьи",
    "save_article": "Сохранить статью",

    "article_constructor": "Конструктор статей",

    "test_checking": "Проверка теста",
    "tires_results": "Результаты попыток",
    "check_try": "Проверить попытку",

    "test_checking_user": "Проверка попытки пользователя",
    "add_comment": "Добавить комментарий",
    "result_": "Результат:",
    "complete_checking": "Завершить проверку",

    "test_editor_of": "Редактор теста",
    "test_editor": "Редактор теста",
    "solo": "Единственный ответ",
    "multiple": "Множественный ответ",
    "free": "Краткий свободный ответ",
    "detailed_free": "Свободный ответ",
    "info_block": "Информационный блок",
    "add_question": "Добавить вопрос",
    "save_test": "Сохранить тест",

    "test_constructor": "Конструктор тестов",

    "access_denied": "Доступ запрещён",
    "but_you_can_subscribe": "Но вы можете получить доступ к материалам данного курса, подписавшись на него",

    "new_note": "Новая заметка",
    "name_": "Название:",
    "note_": "Заметка:",
  },
  'de': {
    'mainpage': 'Startseite',
    'support': 'support',
    'profile': 'Profil',
    'my_profile': 'Mein Profil',
    'my_friends': 'Meine Abonnements',
    'my_subscriptions': 'Meine Kurse',
    'my_achievements': 'Meine Belohnungen',
    'achievements': 'Erfolge',
    'timetable': 'Mein Zeitplan',
    'settings': 'Einstellungen',
    'reviews': 'Bewertungen',
    'aboutus': 'Über uns',
    'exit': 'Beenden',
    'areusure': 'Möchten Sie unbedingt aussteigen?',
    'confirmexit': 'Abmeldung bestätigen',
    'logout': 'Abmelden von Ihrem Konto',
    'flag': 'flag-germany',
    'your_chats': 'Ihre Dialoge',
    'admin': 'administrator',
    'subscribe': 'Abonnieren',
    'unsubscribe': 'Abbestellen',
    'give_admin': 'Administratorberechtigungen erteilen',
    'remove_admin': 'Administratorrechte ablegen',
    'info': 'Weitere Informationen',
    'subscriptions': 'Abonnements',
    'subscriptions_': 'Abonnements',
    'subscribers': 'Abonnenten',
    'participant_in': 'Teilnehmer in',
    'founded_by_request': 'Auf Anfrage gefunden:',

    'users_courses': 'Benutzerdefinierte Kurse',
    'create_course': 'Kurs erstellen',
    'course_creation': 'Kurs erstellen',
    'enter_course_data': 'Kursdaten eingeben:',
    'create': 'Erstellen',

    'createform': 'Formular erstellen',
    'form': 'Form',

    'maininfo': 'Grundlegende Informationen',
    'changeava': 'Avatar ändern',
    'anachievements': 'Erfolge',
    'name': 'Name',
    'surname': 'Nachname',
    'phonenumber': 'Telefonnummer',
    'email': 'E-Mail',
    'city': 'Stadt:',
    'city_': 'Stadt',
    'university': 'Institut',
    'specialization': 'Spezialität',
    'group': 'Lerngruppe',
    'save': 'Speichern',

    'devteam': 'Entwicklerteam',
    'pavel': 'Paul',
    'pavinfo': 'Backend und Frontend Entwickler',
    'online': 'Online',
    'ilya': 'ilya',
    'ilyinfo': 'Frontend-Entwickler',
    'offline': 'Offline',
    'anton': 'Anton',
    'antinfo': 'Backend-Entwickler',
    'afk': 'Schläft',
    'devinfo': 'Entwicklerinformationen',

    'my_notes': 'Meine Notizen',
    'my_tasks': 'Meine Aufgaben',
    'month': 'Monat',

    "monday": "MO",
    "tuesday": "W",
    "wednesday": "MI",
    "thursday": "DO",
    "friday": "FR",
    "saturday": "SA",
    "sunday": "SUN",

    "course": "Kurs",
    "courses": "Kurse",
    "course_rating": "Kursbewertung:",
    "rate_first": "Dieser Kurs wurde noch nicht bewertet, sei der erste!",
    "go_to_course": "Kurs wechseln",
    "edit_course": "Kurs bearbeiten",
    "delete_course": "Kurs löschen",
    "course_participants": "Kursteilnehmer",
    "desc": "Beschreibung",
    "thanks_for_your_feedback": "Vielen Dank für Ihr Feedback!",
    "how_do_you_like_this_course": "Wie gefällt Ihnen dieser Kurs?",
    "give_us_feedback": "Hinterlassen Sie Ihr Feedback:",
    "what_about_comment": "Was ist mit einem Kommentar?",
    "course_participants_feedback": "Feedback der Kursteilnehmer",
    "feedback_without_comment": "--- Feedback ohne Kommentar ---",
    "show_all_feedback": "Alle Erfahrungsberichte anzeigen",
    "confirm_delete_course": "Bestätigung, dass der Kurs gelöscht wird",
    "are_u_sure_delete_course": "Sie möchten den Kurs unbedingt löschen",
    "delete": "Löschen",

    "course_participants_of": "Kursteilnehmer",
    "curator": "KURATOR",
    "give_curator": "Berechtigung zum Kurator erteilen",
    "remove_curator": "Die Autorität des Kurators aufheben",

    "course_content": "Kursinhalte",
    "test": "Test",
    "article": "Artikel",
    "done": "Fertig",
    "checking": "Im Check",
    "not_done": "fehlgeschlagen",
    "show_summary": "Fortschrittsbericht anzeigen",
    "test_desc": "Beantworte die Fragen und erhalte einen Preis",
    "article_desc": "Lesen Sie den Artikel und essen Sie Süßigkeiten",

    "course_summary": "Kursübersicht",
    "course_unit": "Kurselement",
    "tesk_type": "Typ",
    "status": "Status",
    "mark": "Bewertung",
    "unit": "Partition",
    "result": "Ergebnis",
    "unit_result": "Partitionszusammenfassung",

    "read_article": "Artikel wurde gelesen",

    "show_tries": "Versuche anzeigen",
    "leaders_table": "Bestenliste",
    "progress_graphic": "Fortschrittsplan",
    "friends_progress": "Fortschritt von Freunden",
    "last_tries": "Ergebnisse Ihrer vorherigen Versuche",
    "try_number": "Versuchsnummer",
    "condition": "Zustand",
    "viewing": "Anzeigen",
    "time_spent": "Zeitaufwand für das Durchlaufen",
    "show_try": "Versuch ansehen",
    "best_mark": "Höchste Bewertung:",
    "best_mark_": "Höchste Bewertung",
    "place": "Place",
    "user": "Benutzer",
    "graphic_desc": "Zeitplan für die Verteilung der Benutzer nach höchster Bewertung",
    "friends_table_desc": "Die Bestenliste unter den Freunden, denen du abonniert hast",
    "marking_method": "Bewertungsmethode: Lehrer",
    "start_test": "Test starten",

    "try_showing": "Einen Versuch anzeigen",
    "information": "Information",
    "question": "Frage",
    "score": "Punkte:",
    "not_marked": "Nicht bewertet",
    "the_same_answer": "Benutzer haben dieselbe Antwort auf diese Aufgabe gegeben",
    "curator_comment": "Kommentar des Kurators:",
    "your_result": "Ihr Ergebnis ist:",
    "your_time_spent": "Die Zeit ist vergangen ",

    "passing_the_test": "Test bestehen",
    "complete_test": "Test abschließen",

    "course_reviews": "Kursbewertungen",

    "course_editing": "Kurs bearbeiten",
    "check": "Überprüfen",
    "edit": "Bearbeiten",
    "task_creation": "Auftrag erstellen",
    "choose_task_type": "Wählen Sie den Typ des zu erstellenden Auftrags aus:",
    "confirm_delete_unit": "Bestätigung des Löschens einer Partition",
    "confirm_delete_test": "Bestätigung, dass der Test gelöscht wurde",
    "confirm_delete_article": "Bestätigung des Löschens eines Artikels",
    "are_u_sure_delete_unit": "Sie möchten die Partition unbedingt löschen",
    "are_u_sure_delete_test": "Sie möchten den Test unbedingt löschen",
    "are_u_sure_delete_article": "Sie möchten den Artikel unbedingt löschen",
    "unit_creation": "Partition erstellen",
    "enter_unit_name": "Geben Sie einen Namen für die Partition ein:",
    "save_course": "Kurs speichern",

    "article_edit": "Artikel erstellen",
    "enter_article": "Artikel eingeben (in Markdown)",
    "article_text": "Artikeltext",
    "article_preview": "Vorschau Ihres Artikels",
    "save_article": "Artikel speichern",

    "article_constructor": "Artikel-Designer",

    "test_checking": "Test prüfen",
    "tires_results": "Ergebnisse der Versuche",
    "check_try": "Versuch prüfen",

    "test_checking_user": "Benutzerversuch prüfen",
    "add_comment": "Kommentar hinzufügen",
    "result_": "Ergebnis:",
    "complete_checking": "Prüfung abschließen",

    "test_editor_of": "Testeditor",
    "test_editor": "Testeditor",
    "solo": "Die einzige Antwort",
    "multiple": "Multiple Antwort",
    "free": "Kurze freie Antwort",
    "detailed_free": "Freie Antwort",
    "info_block": "Informationsblock",
    "add_question": "Frage hinzufügen",
    "save_test": "Test speichern",

    "test_constructor": "Testkonstruktor",

    "access_denied": "Zugriff verweigert",
    "but_you_can_subscribe": "Sie können jedoch auf den Inhalt dieses Kurses zugreifen, indem Sie ihn abonnieren",

    "new_note": "Neue Notiz",
    "name_": "Name:",
    "note_": "Hinweis:",
    },
    'fr': {
      'mainpage': 'Accueil',
      'support': 'Support',
      'profile': 'Profil',
      'my_profile': 'mon profil',
      'my_friends': 'mes abonnements',
      'my_subscriptions': 'mes cours',
      'my_achievements': 'mes récompenses',
      'achievements': 'Réalisations',
      'timetable': 'mon horaire',
      'settings': 'Paramètres',
      'reviews': 'Avis',
      'aboutus': 'À propos de nous',
      'exit': 'Quitter',
      'areusure': 'voulez-vous vraiment sortir?',
      'confirmexit': 'confirmation de sortie',
      'logout': 'Déconnexion du compte',
      'flag': 'flag-france',
      'your_chats': 'vos dialogues',
      'admin': 'ADMINISTRATEUR',
      'subscribe': 's\'Abonner',
      'unsubscribe': 'se Désabonner',
      'give_admin': 'Accorder des privilèges d\'administrateur',
      'remove_admin': 'Supprimer les privilèges d\'administrateur',
      'info': 'lire la Suite',
      'subscriptions': 'Abonnements',
      'subscriptions_': 'abonnements',
      'subscribers': 'abonnés',
      'participant_in': 'Participant à',
      'founded_by_request': 'trouvé sur demande:',

      'users_courses': 'cours Personnalisés',
      'create_course': 'Créer un cours',
      'course_creation': 'Création d\'un cours',
      'enter_course_data': 'Entrez les données du cours:',
      'create': 'Créer',

      'createform': 'Créer un formulaire',
      'form': 'Forme',

      'maininfo': 'informations de Base',
      'changeava': 'Changer d\'avatar',
      'anachievements': 'Réalisations',
      'name': 'Nom',
      'surname':'nom de Famille',
      'phonenumber': 'Numéro de téléphone',
      'email': 'Email',
      'city': 'Ville:',
      'city_': 'Ville',
      'university': 'Institut',
      'specialization': 'Spécialité',
      'group': 'groupe d\'Étude',
      'save': 'Enregistrer',

      'devteam': 'équipe de développement',
      'pavel': 'Paul',
      'pavinfo': 'backend and Frontend Developer',
      'online': 'en ligne',
      'ilya': 'Ilya',
      'ilyinfo': 'Frontend Developer',
      'offline': 'Offline',
      'anton': 'Anton',
      'antinfo': 'développeur Backend',
      'afk': 'Dort',
      'devinfo': 'informations sur le développeur',

      'my_notes': 'mes notes',
      'my_tasks': 'mes tâches',
      'month': 'Mois',

      "monday": "LUN",
      "tuesday": "W",
      "wednesday": "CF",
      "thursday": "JEUDI",
      "friday": "VEN",
      "saturday": "SAT",
      "sunday": "Sun",

      "course": "Cours",
      "courses": "Cours",
      "course_rating": "Classement du cours:",
      "rate_first": "ce cours n'a pas encore été évalué, soyez le premier!",
      "go_to_course": "Aller au cours",
      "edit_course":"Modifier le cours",
      "delete_course": "Supprimer le cours",
      "course_participants": "Participants au cours",
      "desc": "Description",
      "thanks_for_your_feedback": "Merci pour vos commentaires!",
      "how_do_you_like_this_course": "comment Aimez-vous ce cours?",
      "give_us_feedback": "Donnez votre avis:",
      "what_about_comment": "qu'en est-il du commentaire?",
      "course_participants_feedback": "Commentaires des participants au cours",
      "feedback_without_comment": "- - - Commentaire sans commentaire - - -",
      "show_all_feedback": "Voir tous les commentaires sur le cours",
      "confirm_delete_course": "Confirmation de la suppression du cours",
      "are_u_sure_delete_course":"vous voulez vraiment supprimer le cours",
      "delete": "Supprimer",

      "course_participants_of": "Participants au cours",
      "curator": "CURATOR",
      "give_curator":"Donner l'autorité du conservateur",
      "remove_curator":"Supprimer l'autorité du conservateur",

      "course_content": "Contenu du cours",
      "test": "Test",
      "article": "Article",
      "done": "Terminé",
      "checking": "en cours de vérification",
      "not_done": "échec",
      "show_summary":"Voir le résumé des progrès",
      "test_desc":"Répondez aux questions et obtenez le prix",
      "article_desc": "Lisez l'article et mangez des bonbons",

      "course_summary":"Résumé du cours",
      "course_unit": "élément de cours",
      "tesk_type": "Type",
      "status": "Status",
      "mark": "Score",
      "unit": "Partition",
      "result": "Total",
      "unit_result":"Total de la section",

      "read_article": "Article lu",

      "show_tries": "Afficher les tentatives",
      "leaders_table": "classement",
      "progress_graphic":"Graphique de progression",
      "friends_progress": "Progression des amis",
      "last_tries": "Résultats de vos tentatives précédentes",
      "try_number": "numéro de tentative",
      "condition": "Condition",
      "viewing": "Viewing",
      "time_spent":"temps Passé à passer",
      "show_try": "Voir la tentative",
      "best_mark": "meilleur score:",
      "best_mark_":"meilleur score",
      "place": "Place",
      "user": "Utilisateur",
      "graphic_desc": "Graphique de la répartition des utilisateurs selon l'évaluation la plus élevée",
      "friends_table_desc": "classement des amis auxquels vous êtes abonné",
      "marking_method":"méthode d'évaluation: Enseignant",
      "start_test": "Commencer le test",

      "try_showing":"Afficher la tentative",
      "information": "Information",
      "question": "Question",
      "score": "Scores:",
      "not_marked": "Non évalué",
      "the_same_answer": "les utilisateurs ont donné la même réponse à cette tâche",
      "curator_comment": "Commentaire du conservateur:",
      "your_result": "votre résultat:",
      "your_time_spent": "le temps s'est Écoulé",

      "passing_the_test": "Passer le test",
      "complete_test": "Terminer le test",

      "course_reviews":"Avis sur le cours",

      "course_editing": "Modification du cours",
      "check": "Check",
      "edit": "Modifier",
      "task_creation": "Création d'une tâche",
      "choose_task_type": "Choisissez le type de travail à créer:",
      "confirm_delete_unit": "Confirmation de la suppression de la partition",
      "confirm_delete_test": "Confirmation de la suppression du test",
      "confirm_delete_article": "Confirmation de la suppression de l'article",
      "are_u_sure_delete_unit":"vous voulez vraiment supprimer la partition",
      "are_u_sure_delete_test": "voulez-vous vraiment supprimer le test",
      "are_u_sure_delete_article": "vous voulez vraiment supprimer l'article",
      "unit_creation": "Créer une partition",
      "enter_unit_name": "Entrez le nom de la section:",
      "save_course": "Enregistrer le cours",

      "article_edit": "Rédaction de l'article",
      "enter_article": "Entrée de l'article (dans Markdown)",
      "article_text":"Texte de l'article",
      "article_preview":"Aperçu de votre article",
      "save_article": "Enregistrer l'article",

      "article_constructor":"Constructeur d'articles",

      "test_checking":"Vérification du test",
      "tires_results": "résultats des tentatives",
      "check_try": "Vérifier la tentative",

      "test_checking_user":"Vérification de la tentative de l'utilisateur",
      "add_comment": "Ajouter un commentaire",
      "result_": "Résultat:",
      "complete_checking": "Terminer la vérification",

      "test_editor_of": "Éditeur de test",
      "test_editor":"Éditeur de test",
      "solo": "seule réponse",
      "multiple": "réponse Multiple",
      "free":"réponse Courte et gratuite",
      "detailed_free": "réponse Libre",
      "info_block": "bloc d'Informations",
      "add_question": "Ajouter une question",
      "save_test": "Enregistrer le test",

      "test_constructor":"Constructeur de test",

      "access_denied":"Accès refusé",
      "but_you_can_subscribe":"Mais vous pouvez accéder au contenu de ce cours en vous inscrivant",

      "new_note":"nouvelle Note",
      "name_": "Titre:",
      "note_":"Note:",
    },
    'es': {
      'mainpage':'Inicio',
      'support':'Support',
      'profile':'Perfil',
      'my_profile': 'mi perfil',
      'my_friends' :' mis suscripciones',
      'my_subscriptions' :' mis cursos',
      'my_achievements' :' mis recompensas',
      'achievements': 'Logros',
      'timetable': 'mi horario',
      'settings': 'Ajustes',
      'reviews': 'Reviews',
      'aboutus': 'Sobre nosotros',
      'exit': 'Salir',
      'areusure': '¿seguro que quieres salir?',
      'confirmexit' :' confirmación de salida',
      'logout': 'Cerrar sesión',
      'flag': 'flag-spain',
      'your_chats': 'Tus diálogos',
      'admin':'ADMIN',
      'subscribe':'Suscribirse',
      'unsubscribe':'darse de Baja',
      'give_admin': 'Otorgar privilegios de administrador',
      'remove_admin': 'Deponer privilegios de administrador',
      'info': 'Más información',
      'subscriptions': 'Suscripciones',
      'subscriptions_': 'suscripciones',
      'subscribers': 'suscriptores',
      'participant_in': 'Participante en',
      'founded_by_request': 'Encontrado para:',

      'users_courses': 'cursos Personalizados',
      'create_course': 'Crear curso',
      'course_creation': 'Crear un curso',
      'enter_course_data': 'Introduzca los datos del curso:',
      'create': 'Crear',

      'createform': 'Crear un formulario',
      'form': 'Forma',

      'maininfo': 'información Básica',
      'changeava': 'Cambiar avatar',
      'anachievements': 'Logros',
      'name':'Nombre',
      'surname':'Apellido',
      'phonenumber': 'número de Teléfono',
      'email':'email',
      'city':'Ciudad:',
      'city_':'Ciudad',
      'university':'Instituto',
      'specialization':'Especialidad',
      'group': 'grupo de Estudio',
      'save': 'Guardar',

      'devteam' :' equipo de desarrollo',
      'pavel':'Pablo',
      'pavinfo':'desarrollador de backend y Frontend',
      'online': 'En línea',
      'ilya':'Ilya',
      'ilyinfo': 'desarrollador Frontend',
      'offline': 'Offline',
      'anton': 'Anton',
      'antinfo': 'desarrollador de Backend',
      'afk':'Durmiendo',
      'devinfo': 'Información del desarrollador',

      'my_notes' :' mis notas',
      'my_tasks' :' mis tareas',
      'month': 'Mes',

      "monday": "LUNES",
      "tuesday":"MARTES",
      "wednesday": "MIÉ",
      "thursday": "JUE",
      "friday":"VIERNES",
      "saturday": "SAT",
      "sunday":"SUN",

      "course":"Curso",
      "courses": "Cursos",
      "course_rating": "Clasificación del curso:",
      "rate_first": "este curso aún no ha sido evaluado, ¡sea el primero!",
      "go_to_course": "Ir al curso",
      "edit_course": "Editar curso",
      "delete_course": "Eliminar curso",
      "course_participants": "Participantes del curso",
      "desc":"Descripción",
      "thanks_for_your_feedback": "¡Gracias por tus comentarios!",
      "how_do_you_like_this_course": "¿qué te Parece este curso?",
      "give_us_feedback": "Deja un comentario:",
      "what_about_comment": "¿qué tal un comentario?",
      "course_participants_feedback": "Opiniones de los participantes del curso",
      "feedback_without_comment": "- - - Opinión sin comentarios - - -",
      "show_all_feedback": "Ver todas las reseñas del curso",
      "confirm_delete_course": "confirmación de la eliminación del curso",
      "are_u_sure_delete_course": "seguro que quieres eliminar el curso",
      "delete":"Eliminar",

      "course_participants_of": "Participantes del curso",
      "curator": "CURADOR",
      "give_curator": "Otorgar credenciales de curador",
      "remove_curator": "Deponer los poderes del curador",

      "course_content": "Contenido del curso",
      "test":"Test",
      "article":"Artículo",
      "hecho":"Hecho",
      "checking": "en la verificación",
      "not_done": "No ejecutado",
      "show_summary": "Ver Resumen de progreso",
      "test_desc": "Responde a las preguntas y consigue un premio",
      "article_desc": "Lee el artículo y come un dulce",

      "course_summary": "Resumen del curso",
      "course_unit": "elemento de curso",
      "tesk_type": "Tipo",
      "status":"Status",
      "mark": "Evaluación",
      "unit":"Sección",
      "result":"Resultado",
      "unit_result": "Resumen de la partición",

      "read_article": "Artículo leído",

      "show_tries": "Ver intentos",
      "leaders_table": "tabla de clasificación",
      "progress_graphic": "Gráfico de progreso",
      "friends_progress": "Progreso de amigos",
      "last_tries": "Resultados de tus intentos anteriores",
      "try_number": "número de intento",
      "condition":"Estado",
      "viewing":"Ver",
      "time_spent": "Tiempo perdido",
      "show_try": "Ver intento",
      "best_mark":"Puntuación más Alta:",
      "best_mark_":"Puntuación Más alta",
      "place":"Lugar",
      "user":"Usuario",
      "graphic_desc": "Gráfico de la distribución de usuarios según la Puntuación más alta",
      "friends_table_desc": "clasificación de amigos a los que sigues",
      "marking_method": "Método de evaluación: Profesor",
      "start_test": "Iniciar prueba",

      "try_showing": "Ver intento",
      "information":"Información",
      "question":"Pregunta",
      "score":"Puntos:",
      "not_marked": "No evaluado",
      "the_same_answer": "los usuarios dieron la misma respuesta a esta tarea",
      "curator_comment": "Comentario del curador:",
      "your_result":"tu resultado es:",
      "your_time_spent": "ha Pasado el tiempo ",

      "passing_the_test": "Pasar la prueba",
      "complete_test": "Completar la prueba",

      "course_reviews": "Opiniones sobre el curso",

      "course_editing": "Edición del curso",
      "check":"Check",
      "editar":"Editar",
      "task_creation": "Crear una tarea",
      "choose_task_type": "Seleccione el tipo de trabajo que desea crear:",
      "confirm_delete_unit": "confirmación de eliminación de partición",
      "confirm_delete_test": "confirmación de eliminación de prueba",
      "confirm_delete_article": "confirmación de la eliminación del artículo",
      "are_u_sure_delete_unit": "definitivamente quieres eliminar la partición",
      "are_u_sure_delete_test": "definitivamente quieres eliminar la prueba",
      "are_u_sure_delete_article": "definitivamente quieres eliminar el artículo",
      "unit_creation": "crear una partición",
      "enter_unit_name": "Introduzca el nombre de la sección:",
      "save_course": "Guardar curso",

      "article_edit": "Redacción de un artículo",
      "enter_article": "Introducir un artículo (en Markdown)",
      "article_text": "Texto del artículo",
      "article_preview": "vista Previa de tu artículo",
      "save_article": "Guardar artículo",

      "article_constructor": "constructor de artículos",

      "test_checking": "Comprobación de prueba",
      "tires_results": "Resultados de los intentos",
      "check_try": "Comprobar intento",

      "test_checking_user": "Comprobación del intento del usuario",
      "add_comment": "Añadir un comentario",
      "result_":"Resultado:",
      "complete_checking": "Finalizar comprobación",

      "test_editor_of": "Editor de pruebas",
      "test_editor": "Editor de pruebas",
      "solo": "La única respuesta",
      "multiple": "respuesta Múltiple",
      "free": "Breve respuesta libre",
      "detailed_free":"respuesta Gratuita",
      "info_block": "bloque de Información",
      "add_question": "Añadir pregunta",
      "save_test": "Guardar prueba",

      "test_constructor": "constructor de pruebas",

      "access_denied": "acceso denegado",
      "but_you_can_subscribe": "pero puedes acceder a este curso suscribiéndote a él",

      "new_note":"nueva nota",
      "name_":"Nombre:",
      "note_":"Nota:",
    },
  'pt': {
    'mainpage': 'início',
    'support':'Suporte',
    'perfil':'perfil',
    'my_profile' :' meu perfil',
    'my_friends' :' Minhas Subscrições',
    'my_subscriptions' :' meus cursos',
    'my_achievements' :' minhas recompensas',
    'achievements': 'realizações',
    'timetable': 'minha agenda',
    'settings': 'Configurações',
    'reviews': 'comentários',
    'aboutus': 'Sobre nós',
    'exit': 'sair',
    'areusure': 'tem certeza que quer sair?',
    'confirmexit': 'confirmar a saída',
    'logout': 'Sair da conta',
    'flag': 'flag-portugal',
    'your_chats': 'seus diálogos',
    'admin':'administrador',
    'subscribe': 'subscrever',
    'unsubscribe': 'Cancelar subscrição',
    'give_admin': 'conceder privilégios de administrador',
    'remove_admin': 'remover privilégios de administrador',
    'info': 'Saiba mais',
    'subscriptions': 'Subscrições',
    'subscriptions_': 'Subscrições',
    'subscribers': 'subscritores',
    'participant_in': 'participante em',
    'founded_by_request': 'encontrado por:',

    'users_courses': 'cursos personalizados',
    'create_course': 'criar curso',
    'course_creation': 'criar um curso',
    'enter_course_data': 'introduza os dados do curso:',
    'create': 'Criar',

    'createform': 'criar um formulário',
    'form':'form',

    'maininfo': 'Informação básica',
    'changeava': 'alterar Avatar',
    'anachievements': 'realizações',
    'name':'Name',
    'surname': 'sobrenome',
    'phonenumber': 'número de telefone',
    'email':'email',
    'city':'Cidade:',
    'city_': 'cidade',
    'Universidade': 'Instituto',
    'specialization':'especialidade',
    'group':'Grupo de estudo',
    'save': 'Salvar',

    'devteam': 'equipe de desenvolvimento',
    'pavel': 'Pavel',
    'pavinfo': 'desenvolvedor de back-end e Front-End',
    'online':'no site',
    'ilya': 'Ilya',
    'ilyinfo': 'Desenvolvedor Front-End',
    'offline': 'Offline',
    'anton': 'Anton',
    'antinfo': 'desenvolvedor de back-end',
    'afk': 'dormindo',
    'devinfo': 'informações do desenvolvedor',

    'my_notes' :' minhas notas',
    'my_tasks' :' minhas tarefas',
    'month': 'mês',

    "segunda-feira": "seg",
    "tuesday": "ter",
    "wednesday": "qua",
    "thursday": "qui",
    "sexta-feira": "PT",
    "saturday": "SAT",
    "sunday": "dom",

    "curso": "Curso",
    "Cursos": "Cursos",
    "course_rating": "classificação do curso:",
    "rate_first": "este curso ainda não foi avaliado, seja o primeiro!",
    "go_to_course": "ir para o curso",
    "edit_course": "editar curso",
    "delete_course": "excluir curso",
    "course_participants":"participantes do curso",
    "desc": "Descrição",
    "thanks_for_your_feedback": "obrigado pelo feedback!",
    "how_do_you_like_this_course": "o que você acha deste curso?",
    "give_us_feedback": "deixe seu comentário:",
    "what_about_comment": "e quanto ao comentário?",
    "course_participants_feedback": "comentários dos participantes do curso",
    "feedback_without_comment": "- - - comentário Sem comentários ---",
    "show_all_feedback": "ver todos os comentários do curso",
    "confirm_delete_course": "confirmar a exclusão do curso",
    "are_u_sure_delete_course": "você definitivamente deseja excluir um curso",
    "delete": "Excluir",

    "course_participants_of": "participantes do curso",
    "curator":"curador",
    "give_curator": "emitir Autoridade de curador",
    "remove_curator": "destituir a autoridade do curador",

    "course_content": "conteúdo do curso",
    "test": "Teste",
    "article": "artigo",
    "done": "concluído",
    "checking": "na verificação",
    "not_done": "não concluído",
    "show_summary": "Ver resumo do progresso",
    "test_desc": "responda às perguntas e ganhe um prêmio",
    "article_desc": "leia o artigo e coma um doce",

    "course_summary": "Resumo do curso",
    "course_unit": "elemento do curso",
    "tesk_type": "Tipo",
    "status":"Status",
    "mark": "avaliação",
    "unit": "seção",
    "Resultado":"Resultado",
    "unit_result": "total da seção",

    "read_article": "artigo lido",

    "show_tries": "ver tentativas",
    "leaders_table": "tabela de líderes",
    "progress_graphic": "Gráfico de progresso",
    "friends_progress": "progresso dos amigos",
    "last_tries": "resultados de suas tentativas anteriores",
    "try_number": "número da tentativa",
    "condition": "Estado",
    "viewing": "ver",
    "time_spent": "tempo gasto passando",
    "show_try": "veja a tentativa",
    "best_mark": "nota máxima:",
    "best_mark_": "avaliação Superior",
    "place":"Place",
    "user":"Usuário",
    "graphic_desc": "Gráfico de alocação de usuários por pontuação mais alta",
    "friends_table_desc": "tabela de classificação entre amigos que você segue",
    "marking_method": "método de avaliação: Professor",
    "start_test": "Iniciar teste",

    "try_showing": "ver tentativa",
    "information":"informação",
    "questão":"questão",
    "score":"pontos:",
    "not_marked": "Não avaliado",
    "the_same_answer": "os usuários deram a mesma resposta a esta tarefa",
    "curator_comment": "comentário do curador:",
    "your_result": "seu resultado:",
    "your_time_spent": "o tempo passou ",

    "passing_the_test": "passar no teste",
    "complete_test": "Complete o teste",

    "course_reviews": "comentários do curso",

    "course_editing": "editar curso",
    "check":"Check",
    "editar":"editar",
    "task_creation": "criar uma tarefa",
    "choose_task_type": "selecione o tipo de tarefa a ser criada:",
    "confirm_delete_unit": "confirmar a remoção da partição",
    "confirm_delete_test": "confirmar a remoção do teste",
    "confirm_delete_article": "confirmar a exclusão do artigo",
    "are_u_sure_delete_unit": "você definitivamente deseja excluir a partição",
    "are_u_sure_delete_test": "você definitivamente deseja excluir o teste",
    "are_u_sure_delete_article": "você definitivamente deseja excluir o artigo",
    "unit_creation": "criar partição",
    "enter_unit_name": "digite o nome da partição:",
    "save_course": "salvar curso",

    "article_edit": "elaboração do artigo",
    "enter_article": "inserir um artigo (em Markdown)",
    "article_text": "texto do artigo",
    "article_preview": "pré-visualização do seu artigo",
    "save_article": "salvar artigo",

    "article_constructor": "construtor de artigos",

    "test_checking": "teste de validação",
    "tires_results": "resultados das tentativas",
    "check_try": "verificar tentativa",

    "test_checking_user": "verificação de tentativa do Usuário",
    "add_comment": "Adicionar comentário",
    "result_": "resultado:",
    "complete_checking": "concluir verificação",

    "test_editor_of":"editor de teste",
    "test_editor":"editor de teste",
    "solo": "a única resposta",
    "multiple": "resposta múltipla",
    "free": "Uma breve resposta livre",
    "detailed_free":"resposta Livre",
    "info_block": "Bloco de informações",
    "add_question": "adicionar pergunta",
    "save_test": "salvar teste",

    "test_constructor": "construtor de testes",

    "access_denied": "Acesso negado",
    "but_you_can_subscribe": "mas você pode acessar o conteúdo deste curso inscrevendo-se nele",

    "new_note":"nova nota",
    "name_": "título:",
    "note_": "Nota:",
  },
  'cn':{
    "mainpage":"主页",
    'support':'支持',
    'profile':'个人资料',
    'my_profile':'我的个人资料',
    'my_friends':'我的订阅',
    'my_subscriptions':'我的课程',
    'my_achievements':'我的奖项',
    "achievements":"成就",
    "timetable":"我的时间表",
    'settings':'设置',
    "reviews":"评论",
    "aboutus":'关于我们',
    'exit':'退出',
    'areusure':'你确定要出去吗？',
    'confirmexit':'退出确认',
    'logout':'从账户注销',
    'flag': 'flag-china',
    'your_chats':'你的对话',
    'admin':'行政主任',
    'subscribe':'订阅',
    'unsubscribe':'取消订阅',
    'give_admin':'授予管理员权限',
    'remove_admin':'撤销管理员权限',
    "info":"了解更多",
    'subscriptions':'订阅',
    'subscriptions_':'订阅',
    "subscribers":"订户",
    'participant_in':'参与',
    'founded_by_request':'根据请求找到:',

    'users_courses':'定制课程',
    'create_course':'创建课程',
    'course_creation':'创建课程',
    'enter_course_data':'输入课程数据:',
    'create':'创建',

    'createform':'创建表单',
    'form':'表格',

    'maininfo':'基本信息',
    'changeava':'改变头像',
    "anachievements":"成就",
    'name':'Name',
    'surname':'姓',
    'phonenumber':'电话号码',
    'email':'电子邮件',
    'city':'城市:',
    'city_':'城市',
    'university':'研究所',
    'specialization':'专业',
    'group':'勉強会',
    'save':'保存',

    'devteam':'开发团队',
    'pavel':'帕维尔',
    'pavinfo':'后端和前端开发人员',
    "online":"在网站上",
    'ilya':'伊利亚',
    'ilyinfo':'前端开发人员',
    'offline':'离线',
    'anton':'安东',
    'antinfo':'后端开发人员',
    'afk':'睡觉',
    'devinfo':'开发者信息',

    'my_notes':'我的笔记',
    'my_tasks':'我的任务',
    'month':'月',

    "monday":"星期一",
    "tuesday":"星期二",
    "wednesday":"星期三",
    "thursday":"星期四",
    "friday":"星期五",
    "saturday":"星期六",
    "sunday":"太阳",

    "course":"课程",
    "courses":"课程",
    "course_rating":"课程评分:",
    "rate_first":"这门课程还没有评估，做第一个！",
    "go_to_course":"去课程",
    "edit_course":"编辑课程",
    "delete_course":"删除课程",
    "course_participants":"课程参与者",
    "desc":"描述",
    "thanks_for_your_feedback":"感谢您的反馈！",
    "how_do_you_like_this_course":"你觉得这门课程怎么样？",
    "give_us_feedback":"留下您的反馈：",
    "what_about_comment":"评论怎么样？",
    "course_participants_feedback":"课程参与者的反馈",
    "feedback_without_comment":"---评论不加评论---",
    "show_all_feedback":"查看所有课程评论",
    "confirm_delete_course":"确认课程删除",
    "are_u_sure_delete_course":"你肯定想删除课程",
    "delete":"删除",

    "course_participants_of":"课程参与者",
    "curator":"策展人",
    "give_curator":"授予策展人权力",
    "remove_curator":"撤销馆长权力",

    "course_content":"课程内容",
    "test":"测试",
    "article":"文章",
    "done":"完成",
    "checking":"正在审查中",
    "not_done":"未完成",
    "show_summary":"查看进度摘要",
    "test_desc":"回答问题并获得奖品",
    "article_desc":"阅读文章，吃点糖果",

    "course_summary":"课程总结",
    "course_unit":"课程元素",
    "tesk_type":"类型",
    "status":"状态",
    "mark":"等级",
    "unit":"科",
    "result":"摘要",
    "unit_result":"章节摘要",

    "read_article":"文章已被阅读",

    "show_tries":"查看尝试",
    "leaders_table":"排行榜",
    "progress_graphic":"进度图",
    "friends_progress":"朋友的进步",
    "last_tries":"您之前尝试的结果",
    "try_number":"尝试次数",
    "condition":"状态",
    "viewing":"查看",
    "time_spent":"通过所花费的时间",
    "show_try":"查看尝试",
    "best_mark":"最高分:",
    "best_mark_":"最高分",
    "place":"地方",
    "user":"用户",
    "graphic_desc":"按最高评级划分的用户分布图",
    "friends_table_desc":"您订阅的好友中排行榜",
    "marking_method":"评价方式：老师",
    "start_test":"开始测试",

    "try_showing":"查看尝试",
    "information":"资讯",
    "question":"问题",
    "score":"分数：",
    "not_marked":"未评级",
    "the_same_answer":"用户对此任务给出了相同的答案",
    "curator_comment":"策展人评论:",
    "your_result":"你的结果:",
    "your_time_spent":"时间过去了",

    "passing_the_test":"通过测试",
    "complete_test":"完成测试",

    "course_reviews":"课程评论",

    "course_editing":"编辑课程",
    "check":"检查",
    "edit":"编辑",
    "task_creation":"创建任务",
    "choose_task_type":"选择要创建的任务类型:",
    "confirm_delete_unit":"删除部分的确认",
    "confirm_delete_test":"测试删除的确认",
    "confirm_delete_article":"确认文章删除",
    "are_u_sure_delete_unit":"你肯定想删除部分",
    "are_u_sure_delete_test":"你肯定想删除测试",
    "are_u_sure_delete_article":"你肯定想删除文章",
    "unit_creation":"创建一个部分",
    "enter_unit_name":"输入节的名称:",
    "save_course":"保存课程",

    "article_edit":"文章汇编",
    "enter_article":"文章条目（在Markdown中）",
    "article_text":"文章文本",
    "article_preview":"文章预览",
    "save_article":"保存文章",

    "article_constructor":"文章构造函数",

    "test_checking":"测试检查",
    "tires_results":"尝试结果",
    "check_try":"测试尝试",

    "test_checking_user":"用户尝试验证",
    "add_comment":"添加注释",
    "result_":"结果:",
    "complete_checking":"完成验证",

    "test_editor_of":"测试编辑器",
    "test_editor":"测试编辑器",
    "solo":"单一答案",
    "multiple":"多个答案",
    "free":"简短的免费答案",
    "detailed_free":"免费答案",
    "info_block":"信息块",
    "add_question":"添加问题",
    "save_test":"保存测试",

    "test_constructor":"测试构造函数",

    "access_denied":"访问被拒绝",
    "but_you_can_subscribe":"但您可以通过订阅它来访问本课程的材料",

    "new_note":"新笔记",
    "name_":"标题:",
    "note_":"注：",
  },
  'jp':{
    'mainpage':'ホーム',
    'support':'サポート',
    'profile':'プロフィール',
    'my_profile':'私のプロフィール',
    'my_friends':'マイサブスクリプション',
    'my_subscriptions':'私のコース',
    'my_achievements':'私の賞',
    'achievements':'実績',
    'timetable':'私のスケジュール',
    'settings':'設定',
    'reviews':'レビュー',
    'aboutus':'私たちについて',
    'exit':'出口',
    'areusure':'本当に出て行きたいですか？',
    'confirmexit':'終了確認',
    'logout':'アカウントからログアウト',
    'flag':'flag-japan',
    'your_chats':'あなたの対話',
    'admin':'管理者',
    'subscribe':'購読する',
    'unsubscribe':'登録解除',
    'give_admin':'管理者権限の付与',
    'remove_admin':'管理者の権限を削除します',
    'info':'詳細を見る',
    'subscriptions':'定期購読',
    'subscribtions_':'サブスクリプション',
    'subscribers':'加入者',
    'participant_in':'参加者',
    'founded_by_request':'リクエストに応じて見つかりました:',

    'users_courses':'カスタムコース',
    'create_course':'コースを作成する',
    'course_creation':'コースの作成',
    'enter_course_data':'コースデータの入力:',
    'create':'Create',

    'createform':'フォームの作成',
    'form':'フォーム',

    'maininfo':'基本情報',
    'changeava':'アバターを変更',
    'anachievements':'実績',
    'name':'名前',
    'surname':'姓',
    'phonenumber':'電話番号',
    'email':'メール',
    'city':'市:',
    'city_':'市',
    'university':'研究所',
    'specialization':'専門分野',
    'group':'勉強会',
    'save':'保存',

    'devteam':'開発チーム',
    'pavel':'Pavel',
    'pavinfo':'バックエンドとフロントエンドの開発者',
    'online':'サイト上',
    'ilya':'イリヤ',
    'ilyinfo':'フロントエンド開発者',
    'offline':'オフライン',
    'anton':'アントン',
    'antinfo':'バックエンド開発者',
    'afk':'眠っている',
    'devinfo':'開発者情報',

    'my_notes':'私のノート',
    'my_tasks':'マイタスク',
    'month':'月',

    "monday":"月",
    "tuesday":"火",
    "wednesday":"水曜日",
    "Thursday":"木曜日",
    "Friday":"金曜日",
    "saturday":"土",
    "sunday":"日曜日",

    "course":"コース",
    "courses":"「コース」",
    "course_rating":"コース評価:",
    "rate_first":"このコースはまだ評価されていません。",
    "go_to_course":"コースに移動",
    "edit_course":"コースの編集",
    "delete_course":"コースを削除",
    "course_participants":"コース参加者",
    "desc":"説明",
    "thanks_for_your_feedback":"あなたのフィードバックをありがとう！",
    "how_do_you_like_this_course":"このコースはどのように好きですか？",
    "give_us_feedback":"フィードバックを残してください:",
    "what_about_comment":"コメントはどうですか？",
    "course_participants_feedback":"コース参加者からのフィードバック",
    "feedback_without_comment":"---コメントなしのレビュー---",
    "show_all_feedback":"すべてのコースレビューを表示する",
    "confirm_delete_course":"コース削除の確認",
    "are_u_sure_delete_course":"あなたは間違いなくコースを削除したいです",
    "delete":"削除",

    "course_participants_of":"コース参加者",
    "curator":"キュレーター",
    "give_curator":"学芸員権限を付与する",
    "remove_curator":"キュレーター権限を削除する",

    "course_content":"コースコンテンツ",
    "test":"テスト",
    "article":"記事",
    "done":"完了",
    "checking":"レビュー中",
    "not_done":"完了していません",
    "show_summary":"進行状況の概要を表示する",
    "test_desc":"質問に答えて賞品を手に入れよう",
    "article_desc":"記事を読んでお菓子を食べる",

    "course_summary":"コースの概要",
    "course_unit":"コース要素",
    "tesk_type":"タイプ",
    "status":"ステータス",
    "mark":"「グレード」",
    "unit":"セクション",
    "result":"概要",
    "unit_result":"セクションの概要",

    "read_article":"記事が読み込まれました",

    "show_tries":"ビューの試行",
    "leaders_table":"リーダーボード",
    "progress_graphic":"進捗グラフ",
    "friends_progress":"友達の進捗状況",
    "last_tries":"前回の試行の結果",
    "try_number":"試行番号",
    "condition":"状態",
    "viewing":"表示",
    "time_spent":"通過に費やされた時間",
    "show_try":"ビューの試行",
    "best_mark":"最高スコア:",
    "best_mark_":"最高スコア",
    "place":"Place",
    "user":"ユーザー",
    "graphic_desc":"最高評価によるユーザーの分布のグラフ",
    "friends_table_desc":"あなたが購読している友人の間のリーダーボード",
    "marking_method":"評価方法:教師",
    "start_test":"テストを開始する",

    "try_showing":"試行の表示",
    "information":"情報",
    "question":"質問",
    "score":"スコア:",
    "not_marked":"評価されていません",
    "the_same_answer":"ユーザーはこのタスクに対して同じ答えを出しました",
    "curator_comment":"キュレーターのコメント:",
    "your_result":"あなたの結果:",
    "your_time_spent":"時間が経過しました",

    "passing_the_test":"テストに合格する",
    "complete_test":"テストを完了する",

    "course_reviews":"コースレビュー",

    "course_editing":"コースの編集",
    "check":"チェック",
    "edit":"編集",
    "task_creation":"タスクを作成する",
    "choose_task_type":"作成するタスクのタイプを選択します:",
    "confirm_delete_unit":"セクションの削除の確認",
    "confirm_delete_test":"テストの削除の確認",
    "confirm_delete_article":"記事削除の確認",
    "are_u_sure_delete_unit":"セクションを確実に削除したい",
    "are_u_sure_delete_test":"テストを削除します",
    "are_u_sure_delete_article":"あなたは間違いなく記事を削除したいです",
    "unit_creation":"セクションを作成する",
    "enter_unit_name":"セクションの名前を入力します:",
    "save_course":"コースを保存",

    "article_edit":"記事の編集",
    "enter_article":"記事エントリ(Markdown内)",
    "article_text":"記事テキスト",
    "article_preview":"記事のプレビュー",
    "save_article":"記事を保存",

    "article_constructor":"アーティクルコンストラクタ",

    "test_checking":"テストチェック",
    "tires_results":"試行結果",
    "check_try":"テストの試行",

    "test_checking_user":"ユーザーが検証を試みました",
    "add_comment":"コメントを追加",
    "result_":"結果:",
    "complete_checking":"完全な検証",

    "test_editor_of":"テストエディタ",
    "test_editor":"テストエディタ",
    "solo":"単一の答え",
    "multiple":"複数の回答",
    "free":"短い自由回答",
    "detailed_free":"フリーアンサー",
    "info_block":"情報ブロック",
    "add_question":"質問を追加",
    "save_test":"テストを保存",

    "test_constructor":"テストコンストラクタ",

    "access_denied":"アクセスが拒否されました",
    "but_you_can_subscribe":"しかし、あなたはそれを購読することによって、このコースの材料にアクセスすることができます",

    "new_note":"新しいノート",
    "name_":"タイトル:",
    "note_":"ノート:",
    },
}

  $(function() {
    $('.translate').click(function() {
      var lang = $(this).attr('id');
      $('.lang').each(function(index, item) {
        $(this).text(arrLang[lang][$(this).attr('key')]);
		$('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').removeClass('flag-germany').removeClass('flag-france').removeClass('flag-spain').removeClass('flag-portugal').removeClass('flag-china').removeClass('flag-japan').addClass(arrLang[lang][$('.curflag').attr('key')]);
      });
		if (lang == "en"){
			document.getElementById("ru-tick").style.visibility = "hidden";
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
			document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "visible";
			localStorage.setItem('language', 'en')
		} else if(lang == "ru") {
			document.getElementById("ru-tick").style.visibility = "visible";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("de-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'ru')
		} else if(lang == "de") {
			document.getElementById("de-tick").style.visibility = "visible";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'de')
		} else if(lang == "fr") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "visible";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'fr')
		} else if(lang == "es") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "visible";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'es')
		} else if(lang == "pt") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "visible";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'pt')
		} else if(lang == "cn") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "visible";
			document.getElementById("jp-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'cn')
		} else if(lang == "jp") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
            document.getElementById("pt-tick").style.visibility = "hidden";
			document.getElementById("cn-tick").style.visibility = "hidden";
			document.getElementById("jp-tick").style.visibility = "visible";
			localStorage.setItem('language', 'jp')
		}
    });
  });

  let lang = localStorage.getItem('language');
  if(lang.valueOf() == 'en'.valueOf()){
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "visible";
  } else if(lang.valueOf() == 'ru'.valueOf()){
      document.getElementById("ru-tick").style.visibility = "visible";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
  } else if(lang.valueOf() == 'de'.valueOf()){
      document.getElementById("de-tick").style.visibility = "visible";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
  } else if(lang.valueOf() == 'fr'.valueOf()){
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "visible";
  } else if(lang.valueOf() == 'es'.valueOf()){
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "visible";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
  } else if(lang == "pt") {
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "visible";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "hidden";
  } else if(lang == "cn") {
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "visible";
      document.getElementById("jp-tick").style.visibility = "hidden";
  } else if(lang == "jp") {
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("pt-tick").style.visibility = "hidden";
      document.getElementById("cn-tick").style.visibility = "hidden";
      document.getElementById("jp-tick").style.visibility = "visible";
  }
  $('.lang').each(function(index, item) {
      $(this).text(arrLang[lang][$(this).attr('key')]);
      $('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').removeClass('flag-germany').removeClass('flag-france').removeClass('flag-spain').removeClass('flag-portugal').removeClass('flag-china').removeClass('flag-japan').addClass(arrLang[lang][$('.curflag').attr('key')]);
  });