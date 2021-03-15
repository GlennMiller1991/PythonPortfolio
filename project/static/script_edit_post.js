    let paragraph_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[p]' + text.substring(carriageStart, carriageEnd) + '[/p]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }
    let bold_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[b]' + text.substring(carriageStart, carriageEnd) + '[/b]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let italic_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[i]' + text.substring(carriageStart, carriageEnd) + '[/i]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let strike_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[s]' + text.substring(carriageStart, carriageEnd) + '[/s]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let details_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[d]' + text.substring(carriageStart, carriageEnd) + '[/d]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let code_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[c]' + text.substring(carriageStart, carriageEnd) + '[/c]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let pre_func = function() {
        let post_form_edit = document.getElementById('edit_post_form');
        let text = post_form_edit.value;
        let carriageStart = post_form_edit.selectionStart;
        let carriageEnd = post_form_edit.selectionEnd;
        let temp_text = text.substring(0, carriageStart) + '[pre]' + text.substring(carriageStart, carriageEnd) + '[/pre]' + text.substring(carriageEnd);
        post_form_edit.value = temp_text;
    }

    let button_paragraph = document.getElementById('paragraph_button');
    button_paragraph.onclick = paragraph_func;

    let button_bold = document.getElementById('bold_button');
    button_bold.onclick = bold_func;

    let button_italic = document.getElementById('italic_button');
    button_italic.onclick = italic_func;

    let button_strike = document.getElementById('strike_button');
    button_strike.onclick = strike_func;

    let button_details = document.getElementById('details_button');
    button_details.onclick = details_func;

    let button_code = document.getElementById('code_button');
    button_code.onclick = code_func;

    let button_pre = document.getElementById('pre_button');
    button_pre.onclick = pre_func;
