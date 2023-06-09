
$(document).ready(function() {

    // ADD EVENTS LISTENERS to elements


    // switch element form for title, thumbnail
    const elementsIds = new Array('title', 'thumbnail', 'description', 'details');
    switchElementForms(elementsIds);


    // on 'add new section' button click show popUp to add new section
    const addNewSectionBtn = document.getElementById('add-section-btn');
    addNewSectionBtn.addEventListener('click', () => {
        createPopUp('add-section');
    });


    // on section 'edit' button click show popUp to edit section
    const editSectionButtons = document.getElementsByClassName('edit-section-btn');
    for (let btn of editSectionButtons) {
        btn.addEventListener('click', () => {

            // section to edit Id
            const sectionToEditId = btn.getAttribute('sectionId');

            // show current section value in form
            const sectionEditTitle = document.getElementsByClassName('edit-section-title')[0];
            sectionEditTitle.value = btn.getAttribute('title');
            const sectionEditNumber = document.getElementsByClassName('edit-section-number')[0];
            sectionEditNumber.value = btn.getAttribute('number');

            createPopUp('edit-section');

            // POST section to edit Id
            const request = new XMLHttpRequest();
            request.open('POST',`/dashboard/section_to_edit_id/${sectionToEditId}`);
            request.send();
        });
    }


    // on delete section btn click show popup to confirm action
    const deleteSectionButtons = document.getElementsByClassName('delete-section-btn');
    for (let btn of deleteSectionButtons) {
        btn.addEventListener('click', () => {

            // section to delete Id
            const sectionToDeleteId = btn.getAttribute('sectionId');

            // show current section value in form
            const confirmationMessage = document.querySelector('.confirmation-message');
            confirmationMessage.textContent = `Do you want to delete '${btn.getAttribute('title')},
                 section ${btn.getAttribute('number')}'?`;

            createPopUp('confirmation');

            // POST section to delete Id
            const request = new XMLHttpRequest();
            request.open('POST',`/dashboard/delete_section/${sectionToDeleteId}`);
            request.send();
        });
    }

    // on delete file btn click show popup to confirm action
    const deleteFileButtons = document.getElementsByClassName('delete-file-btn');
    for (let btn of deleteFileButtons) {
        btn.addEventListener('click', () => {

            // file to delete Id
            const fileToDeleteId = btn.getAttribute('fileId');

            // display message
            const confirmationMessage = document.querySelector('.confirmation-message');
            const fileTitle = btn.parentNode.querySelector('div').textContent;
            confirmationMessage.textContent = `Do you want to delete '${fileTitle}'?`;

            createPopUp('confirmation');

            // POST file to delete Id
            const request = new XMLHttpRequest();
            request.open('POST',`/dashboard/delete_file/${fileToDeleteId}`);
            request.send();
        });
    }

    // on click file title show popup to edit file
    const editFileButtons = document.getElementsByClassName('file-edit-btn');
    for (let btn of editFileButtons) {
        btn.addEventListener('click', () => {

            // file to delete Id
            const fileToEditId = btn.getAttribute('fileId');

            // request file data

            const xhr = new XMLHttpRequest();

            xhr.open('GET', `/dashboard/get_file_data/${fileToEditId}`);

            xhr.onload = () => {

                let response = JSON.parse(xhr.responseText);

                // if request was successful
                if (response['status'] == 'success') {

                    // show current file value in form
                    $('.file-title-edit').attr('value', response['title']);
                    $('.file-number-edit').attr('value', response['number']);
                    $('.file-description-edit').text(response['description']);
                    $('.edit-restrict-access').attr('checked', response['restrict_access']);
                    $('.change-upload').attr('href', `/dashboard/change_upload/${response['link']}/${fileToEditId}`);
                    
                    createPopUp('edit-file');
                }
            }

            xhr.send();

        });
    }

    // on delete course btn click show popup to confirm action
    const deleteCourseButtons = document.getElementsByClassName('delete-course-btn');
    for (let btn of deleteCourseButtons) {
        btn.addEventListener('click', () => {

            // show current course value in form
            const confirmationMessage = document.querySelector('.confirmation-message');
            const courseTitle = btn.getAttribute('course-title');
            confirmationMessage.textContent = `Do you want to delete '${courseTitle}'?`;

            createPopUp('confirmation');

            // POST course to delete
            const request = new XMLHttpRequest();
            request.open('POST',`/dashboard/delete_course/${courseTitle}`);
            request.send();
        });
    }

});

// switch clicked elements for form to change the element
function switchElementForms(elementsIds) {

    for (let id of elementsIds) {

        const editElement = document.getElementById(id);
        const parentElement = editElement.parentNode;
        const editForm = parentElement.querySelector('form');

        // add exit button to edit form
        const exitBtn = document.createElement('input');
        exitBtn.type = 'button'
        exitBtn.value = 'Exit';
        exitBtn.classList.add('btn', 'transparent-btn');
        editForm.appendChild(exitBtn);

        exitBtn.addEventListener('click', () => {
            // show edit element
            editElement.style.display = 'block';

            // hide edit form
            editForm.style.display = 'none';
        })

        editElement.addEventListener('click', () => {
            // show edit form
            editForm.style.display = 'block';
            
            // hide edit element
            editElement.style.display = 'none';
        });

        // switch to form so can form displays an error message
        // get error div if any
        const errorDiv = editForm.querySelectorAll('.error'); 
        // if any show form and error
        if (errorDiv.length > 0) { 
            // show edit form
            editForm.style.display = 'block';
            
            // hide edit element
            editElement.style.display = 'none';
        }
        
    }
}


// create popUp for element with 'elementId'
function createPopUp(elementId) {

    const popUp = document.createElement('div');
    popUp.classList.add('popup');

    // back button
    const backBtn = document.createElement('input');
    popUp.appendChild(backBtn);

    backBtn.outerHTML = '<input class="btn back-btn" type="button" value="&rarr;" onclick="removePopup();">';

    // get add section form from html and clone it to popUp
    const HTMLform = document.getElementById(elementId);
    const clonedForm = HTMLform.cloneNode(true);
    clonedForm.style.display = 'block';
    popUp.appendChild(clonedForm);

    // place popUp on top
    document.body.appendChild(popUp);
}

// remove popUp from document
function removePopup() {
    const popUp = document.body.getElementsByClassName('popup')[0];
    popUp.remove();
}
