$(function () {
    const teamPageId = $('#team-page-id').val();

    // 저장 버튼 
    $(document).on('click', '#curriculum-save-btn', function () {
        const newCurriculum = $('#curriculum-input').val().trim();
        if (!newCurriculum) {
            alert('커리큘럼을 입력해주세요');
            return;
        }
    
        $.ajax({
            url: `/api/team_pages/${teamPageId}/curriculum`,
            method: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify({ curriculum: newCurriculum }),
            success: function (res) {
                $('#curriculum-input').replaceWith(`<span id="curriculum-text">${res.curriculum}</span>`);
                $('#curriculum-save-btn').text('수정').attr('id', 'curriculum-edit-btn')
                    .removeClass('is-primary').addClass('button is-small is-link is-light ml-2');
            },
            error: function (xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });

    // 수정 버튼 -> 입력창으로 전환
    $(document).on('click', '#curriculum-edit-btn', function () {
        const currentText = $('#curriculum-text').text().trim();
        $('#curriculum-text').replaceWith(`<input type="text" id="curriculum-input" class="input">`);
        $('#curriculum-input').val(currentText); // XSS 방지를 위해 val()로 따로 넣음 
        $(this).text('저장').attr('id', 'curriculum-save-btn')
            .removeClass('is-link is-light').addClass('button is-primary');
    });
});