
// progress bar

$(document).ready(function() {
            
    $('form#upload-file').on('submit', function(event) {

        event.preventDefault();

        // get url info to upload file to
        const chnageUploadInfoDiv =  document.querySelector('.change');
        const fileId = chnageUploadInfoDiv.getAttribute('fileId');
        const link = chnageUploadInfoDiv.getAttribute('link');

        // get file to upload
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
            url: `/dashboard/change_upload/${link}/${fileId}`,
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                // update change_upload page
                // rewriting page with response from request
                document.open();
                document.write(response);
                document.close();
                // scroll window to top
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        });
    });
});