
// enable progress bar
$(document).ready(function() {
            
    $('form#upload-file').on('submit', function(event) {

        event.preventDefault();

        // 
        let fileTypeInput = $('#fileTypeInput')[0].value;
        let fileInputType = $('#fileInput')[0].files[0].type;
        if (!fileInputType.includes(fileTypeInput))
        {

            let errDiv = document.createElement('div');
            errDiv.classList.add('error');
            errDiv.textContent = 'The file you chose to upload does not \
                match the file type you selected.';
            $('#fileInput')[0].parentNode.appendChild(errDiv);
            $('#fileInput')[0].classList.add('is-invalid');

            return 1;
        }

        // get url info to upload file to
        const uploadFileInfoDiv =  document.querySelector('.uploadto');
        const sectionId = uploadFileInfoDiv.getAttribute('sectionid');
        const link = uploadFileInfoDiv.getAttribute('link');

        const formData = new FormData($('form#upload-file')[0]);

        // post form data to upload_file route
        $.ajax({
            xhr: () => {

                const xhr = new XMLHttpRequest();

                // get progress of upload
                xhr.upload.addEventListener('progress', (e) => {

                    // check if file have a length and show progress bar
                    if (e.lengthComputable) { 

                        let percentage = Math.round((e.loaded / e.total) * 100);

                        // show percentage in progress bar
                        $('#progressBar').attr('aria-valuenow', percentage)
                        .css('width', percentage + '%').text(percentage + '%');
                    }
                });

                return xhr;
            },
            type: 'POST',
            url: `/dashboard/upload_file/${link}/${sectionId}`,
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                // update upload_file page
                // rewriting page with response from request
                document.open();
                document.write(response);
                document.close();

                // scroll window to top
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        });

        return;
    });
});