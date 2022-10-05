// PARSED FILES UPDATER

const jsonplaceholder_url = 'https://jsonplaceholder.typicode.com/users'
const total_docs = 10

let filename = 'filename'
let short_file_name = 'short name'//filename.slice(0, 20)

let new_file_template = `<div class="col">
                        <div class="card">
        <img src="/static/imgs/word.png" class="card-img-top" alt="...">
                                            </div>
                                            </div>
`

function add_new_doc() {
    let mock_card = document.getElementById('uploaded_files_list')
    mock_card.insertAdjacentHTML('beforeend', new_file_template)


}

function submit_dropzone_files() {
    console.log('clecked')
    let real_input = document.getElementById('real_submit')
    real_input.click()

}


// setInterval(() => {
//     return fetch(url).then((resp) => {
//         return resp.json()
//     }).then((quote) => {

//         let quote_html = `<h1 id="quote">${quote['quote']}</h1>`
//         let doc_quote = document.getElementById('quote')
//         doc_quote.innerHTML = quote_html

//     })


// }, 3000)


