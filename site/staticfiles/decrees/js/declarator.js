
function cross_btn_remover(){
    // убирает крестик из поля выбора даты, если дата не выбрана
    date_from = document.getElementsByClassName('date_from')[0].value
    if (!date_from){
        close_btn = document.getElementsByClassName('close_date_button from')[0]
        close_btn.setAttribute('hidden', 'hidden')
    }

    date_to = document.getElementsByClassName('date_to')[0].value
    if (!date_to){
        close_btn = document.getElementsByClassName('close_date_button to')[0]
        close_btn.setAttribute('hidden', 'hidden')
    }
    
}

cross_btn_remover()