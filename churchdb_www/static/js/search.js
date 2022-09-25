{
    let form = document.getElementById("form")
    form.onsubmit = onSearch
}

function clearResults() {
    $('#results_tbody').html(``)
}

MAPPA_TIPI = {
    'baptismal': 'Battesimo',
    'first_communion': 'Prima comunione',
    'confirmation': 'Cresima',
    'death': 'Morte',
    'marriage': 'Matrimonio',
    'person': 'Persona'
}

function createLinkTable(link, label, rowspan = null) {
    let td = document.createElement('td')
    td.setAttribute('class', 'text-center')
    td.classList.add('align-middle')
    td.innerHTML = `<a href="${link}">${label}</a>`

    if (rowspan !== null) {
        td.setAttribute('rowspan', rowspan)
    }

    return td
}

function appendResult(result) {
    let tr = document.createElement('tr');
    let tr_marriage = document.createElement('tr');

    let td = document.createElement('td')
    td.setAttribute('scope', 'row')
    td.setAttribute('class', 'text-center')
    td.innerText = MAPPA_TIPI[result.type]

    if (result['type'] === 'marriage') {
        td.setAttribute('rowspan', '2')
        td.classList.add('align-middle')
    }

    tr.appendChild(td)

    let columns = ['first_name', 'last_name', 'fiscal_code']
    columns.forEach(element => {
        let td = document.createElement('td')
        td.setAttribute('class', 'text-center')

        if (result['type'] !== 'marriage' && result['type'] !== 'person') {
            td.innerText = result.released_to_person[element]
        } else if (result['type'] !== 'person') {
            td.innerText = result.released_to_person_1[element]
        } else {
            td.innerText = result[element]
        }

        tr.append(td) 
    });

    if (result['type'] === 'marriage') {
        columns.forEach(element => {
            let td_marriage = document.createElement('td')
            td_marriage.setAttribute('class', 'text-center')
            td_marriage.innerText = result.released_to_person_2[element]
            tr_marriage.appendChild(td_marriage)
        })
    }

    let view_link = "#"
    if (result['type'] === 'person') {
        view_link = `/view/person/${result['id']}`
    }

    tr.append(createLinkTable(view_link, 'View', ((result['type'] === 'marriage') ? '2' : '1')))
    tr.append(createLinkTable('#', 'Export', ((result['type'] === 'marriage') ? '2' : '1')))

    document.getElementById('results_tbody').appendChild(tr);
    if (result['type'] === 'marriage') {
        document.getElementById('results_tbody').appendChild(tr_marriage);
    }
}

function onSearch(ev) {    
    ev.preventDefault()

    let form = document.getElementById("form");

    $.ajax({
        url: "get_results",
        data: new FormData(form),
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        success: ({ results }) => {
            clearResults()
            results.forEach(appendResult)
        }
    })

    return false
}