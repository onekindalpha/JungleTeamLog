$(function () {
    const teamPageId = $('#team-page-id').val();

    // 등록/수정 버튼 클릭 → 입력창으로 전환
    $('#wil-list').on('click', '.wil-edit-btn', function () {
        const $li = $(this).closest('.wil-item');
        const $urlSpan = $li.find('.wil-url');
        const currentUrl = $urlSpan.find('a').attr('href') || '';  // 기존 값 있으면 꺼내오고, 없으면 빈 값

        $urlSpan.html(`<input type="text" class="wil-url-input" value="${currentUrl}" placeholder="블로그 URL을 입력하세요">`);
        $(this).text('저장').removeClass('wil-edit-btn').addClass('wil-save-btn');
    });

    // 저장 버튼 클릭 → PATCH 요청
    $('#wil-list').on('click', '.wil-save-btn', function () {
        const $li = $(this).closest('.wil-item');
        const newUrl = $li.find('.wil-url-input').val().trim();

        $.ajax({
            url: `/api/team_pages/${teamPageId}/wil`,
            method: 'POST',   // upsert이므로 POST 하나로 처리 (라우터에서 upsert 로직으로)
            contentType: 'application/json',
            data: JSON.stringify({ url: newUrl }),
            success: function (res) {
                if (res.url) {
                $li.find('.wil-url').html(`<a href="${res.url}" target="_blank">${res.url}</a>`);
                } else {
                $li.find('.wil-url').html('미등록');
                }
                const btnText = res.url ? '수정' : '등록';
                $li.find('.wil-save-btn').text(btnText).removeClass('wil-save-btn').addClass('wil-edit-btn');
            },
            error: function (xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });
});