const fiscalCodeRegex = /^(?:\w|\d){16}$/g
const nameRegex = /^(?:[a-z]|[A-Z]){1,30}$/g
const phoneRegex = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/g
const emailRegex = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/g

function addValidToID(id) {
    if (!$(id).hasClass('is-valid'))
        $(id).addClass('is-valid')

    removeInvalidFromID(id)
}

function addInvalidToID(id) {
    if (!$(id).hasClass('is-invalid'))
        $(id).addClass('is-invalid')

    removeValidFromID(id)
}

function removeValidFromID(id) {
    if ($(id).hasClass('is-valid'))
        $(id).removeClass('is-valid')
}

function removeInvalidFromID(id) {
    if ($(id).hasClass('is-invalid'))
        $(id).removeClass('is-invalid')
}

function clearStatusFromID(id) {
    removeValidFromID(id)
    removeInvalidFromID(id)
}

function isIDEmpty(id) {
    return $(id).val() === ''
}

function testIdFor(id, regex) {
    let value = $(id).val()
    if (value === '')
        return true

    let result = regex.test(value);
    regex.exec(value)
    return result
}

function inputChecker(id, regex) {
    if (isIDEmpty(id)) {
        clearStatusFromID(id)
        return
    }

    let success = testIdFor(id, regex)

    if (success) {
        addValidToID(id)
        return true
    } else {
        addInvalidToID(id)
        return false
    }
}

$('#fiscal_code_input').change(() => {
    inputChecker('#fiscal_code_input', fiscalCodeRegex)
})

$('#first_name_input').change(() => {
    inputChecker('#first_name_input', nameRegex)
})

$('#last_name_input').change(() => {
    inputChecker('#last_name_input', nameRegex)
})

$('#birth_date_input').change(() => {
    if(!isIDEmpty('#birth_date_input')) {
        addValidToID('#birth_date_input')
    } else {
        clearStatusFromID('#birth_date_input')
    }
})

$('#email_address_input').change(() => {
    inputChecker('#email_address_input', emailRegex)
})

$('#phone_number_input').change(() => {
    inputChecker('#phone_number_input', phoneRegex)
})

$('#form').on('submit', (ev) => {
    let valid = inputChecker('#fiscal_code_input', fiscalCodeRegex) && inputChecker('#first_name_input', nameRegex) && inputChecker('#last_name_input', nameRegex) && inputChecker('#email_address_input', emailRegex) && inputChecker('#phone_number_input', phoneRegex)

    if (!valid) {
        ev.invalid = true

        ev.preventDefault()
        ev.stopPropagation()

        return false
    }

    ev.invalid = false

    return true
})