
// display file when file title is click
// file is displayed under the file title

const viewFileBtn = document.body.querySelectorAll('.view-file');


// remove already displayed file
function removeFile(e) {
    const btn = e.target;
    const fileDiv = btn.parentNode;
    const fileDisplay = fileDiv.querySelector('.file-display');
    fileDisplay.remove();
    const fileDescriptionDiv = fileDiv.querySelector('.file-description');
    fileDescriptionDiv.remove();
    const fileDlBtn = fileDiv.querySelector('.file-dl-btn'); // get file's download btn
    fileDlBtn.remove();

    // display file if title is clicked again
    btn.removeEventListener('click', removeFile);
    btn.addEventListener('click', displayFile);
}


// display file
function displayFile(e){

    // get id form btn
    const btn = e.target;
    const fileId = btn.getAttribute('fileId');
        
    // request for file path
    $.get(`/course/get_file_info/${fileId}`, (fileInfo) => {

        const filePath = fileInfo['filepath'];
        const fileType = fileInfo['filetype'];

        // DISPLAY FILE
        const fileDiv = btn.parentNode;

        // video file
        if (fileType == 'video') {
            const videoPlayer = document.createElement('video');
            videoPlayer.controls = true;
            videoPlayer.src = `/course/file/${filePath}`;
            videoPlayer.classList.add('file-display');
            fileDiv.appendChild(videoPlayer);

        }

        // audio file
        else if (fileType == 'audio') {
            const audioPlayer = document.createElement('audio');
            audioPlayer.controls = true;
            audioPlayer.src = `/course/file/${filePath}`;
            audioPlayer.classList.add('file-display');
            fileDiv.appendChild(audioPlayer);

        }

        // download pdf
        else if (fileType == 'pdf') {
            const pdfDownloadLink = document.createElement('a');
            pdfDownloadLink.href = `/course/file/${filePath}`;
            // pdfDownloadLink.setAttribute('download', 'file');
            pdfDownloadLink.setAttribute('target', '_blank');
            pdfDownloadLink.click();
        }
        
        // description
        const descriptionDiv = document.createElement('div');
        descriptionDiv.classList.add('file-description');
        descriptionDiv.textContent = fileInfo['description'];
        fileDiv.appendChild(descriptionDiv);

        // download btn
        const dlLink = document.createElement('a');
        dlLink.classList.add('file-dl-btn', 'link')
        dlLink.textContent = 'DOWNLOAD';
        dlLink.href = `/course/file/${filePath}`;
        dlLink.setAttribute('download', 'file');
        dlLink.setAttribute('target', '_blank');
        fileDiv.appendChild(dlLink);

        // remove display if title is clicked again
        btn.removeEventListener('click', displayFile);
        btn.addEventListener('click', removeFile);
    });
}

for (let btn of viewFileBtn) {
    btn.addEventListener('click', displayFile);
}