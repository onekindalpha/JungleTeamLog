$(function () {
  const teamPageId = $('#team-page-id').val();

  // "목표 추가" → POST로 새 목표 등록
  $('#goal-add-btn').on('click', function () {
    const competency = $('#competency-select').val();
    const goalText = $('#goal-text-input').val().trim();

    if (!competency || !goalText) {
      alert('핵심역량과 목표 내용을 모두 입력해주세요');
      return;
    }

    $.ajax({
      url: `/api/team_pages/${teamPageId}/goals`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ competency: competency, goal_text: goalText }),
      success: function (res) {
        const g = res.goal;
        const html = `
          <li class="goal-item" data-id="${g._id}">
            <span class="goal-competency">[${g.competency}]</span>
            <span class="goal-text">${g.goal_text}</span>
            <button class="goal-edit-btn">수정</button>
            <button class="goal-delete-btn">삭제</button>
          </li>
        `;
        $('#goal-list').append(html);
        $('#goal-text-input').val('');
        $('#competency-select').val('');
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });

    // "수정" 클릭 → 입력창으로 전환
    $('#goal-list').on('click', '.goal-edit-btn', function () {
        const $li = $(this).closest('.goal-item');
        const currentText = $li.find('.goal-text').text().trim();

        $li.find('.goal-text').replaceWith(`<input type="text" class="goal-edit-input" value="${currentText}">`);
        $(this).text('저장').removeClass('goal-edit-btn').addClass('goal-save-btn');
    });

    // "저장" 클릭 → PATCH로 수정 반영 
    $('#goal-list').on('click', '.goal-save-btn', function () {
        const $li = $(this).closest('.goal-item');
        const goalId = $li.data('id');
        const newGoalText = $li.find('.goal-edit-input').val().trim();

        if (!newGoalText) {
        alert('목표 내용을 입력해주세요');
        return;
        }

        $.ajax({
        url: `/api/goals/${goalId}`,
        method: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify({ goal_text: newGoalText }),
        success: function (res) {
            $li.find('.goal-edit-input').replaceWith(`<span class="goal-text">${res.goal_text}</span>`);
            $li.find('.goal-save-btn').text('수정').removeClass('goal-save-btn').addClass('goal-edit-btn');
        },
        error: function (xhr) {
            alert(xhr.responseJSON.error);
        }
        });
    });

    // 삭제
    $('#goal-list').on('click', '.goal-delete-btn', function () {
        const $li = $(this).closest('.goal-item');
        const goalId = $li.data('id');

        if (!confirm('삭제하시겠습니까?')) return;

        $.ajax({
        url: `/api/goals/${goalId}`,
        method: 'DELETE',
        success: function () {
            $li.remove();
        },
        error: function (xhr) {
            alert(xhr.responseJSON.error);
        }
        });
    });


    $('#achievement-check-btn').on('click', function () {
        const $formArea = $('#achievement-form-area');

        if ($formArea.is(':visible')) {
            $formArea.hide();
            return;
        }

        // 펼칠 때마다, #goal-list의 "현재 상태"를 기준으로 폼을 새로 그림
        $formArea.empty();
        $('.goal-item').each(function () {
            const goalId = $(this).data('id');
            const competency = $(this).find('.goal-competency').text();
            const goalText = $(this).find('.goal-text').text();
            // 현재 이미 저장된 달성률/메모
            const currentRate = $(this).data('rate');
            const currentNote = $(this).data('note') || '';

            // 각 버튼마다 "이 버튼이 현재 선택된 값과 같은지" 확인해서 클래스 결정
            const rates = [0, 25, 50, 75, 100];
            let buttonsHtml = '';  

            for (let i = 0; i < rates.length; i++) {
                const r = rates[i];  // 0, 25, 50, 75, 100을 순서대로 하나씩

                // 이 버튼이 "현재 선택된 값"과 같은지 확인
                let isSelected = '';
                if (currentRate !== '' && parseInt(currentRate) === r) {
                    isSelected = 'selected';
                }

                // 버튼 하나의 HTML을 만들어서, 기존 문자열 뒤에 이어붙임
                buttonsHtml = buttonsHtml + `<button class="rate-btn ${isSelected}" data-rate="${r}">${r}%</button>`;
            }
            
            const html = `
            <div class="achievement-item" data-id="${goalId}">
                <p>${competency} ${goalText}</p>
                <div class="rate-buttons">
                    ${buttonsHtml}
                </div>
                <input type="text" class="achievement-note-input" placeholder="메모" value="${currentNote}">
                <button class="achievement-save-btn">저장</button>
            </div>
            `;
            $formArea.append(html);
        });

        $formArea.show();
    });

    // 0/25/50/75/100 버튼 클릭 → 선택 표시
    $('#achievement-form-area').on('click', '.rate-btn', function () {
        const $item = $(this).closest('.achievement-item');
        $item.find('.rate-btn').removeClass('selected');
        $(this).addClass('selected');
    });

    // 저장 버튼 클릭 → PATCH 요청
    $('#achievement-form-area').on('click', '.achievement-save-btn', function () {
        const $item = $(this).closest('.achievement-item');
        const goalId = $item.data('id');
        const $selectedRate = $item.find('.rate-btn.selected');
        const note = $item.find('.achievement-note-input').val().trim();

        if ($selectedRate.length === 0) {
            alert('달성률을 선택해주세요');
            return;
        }

        const rate = parseInt($selectedRate.data('rate'));

        $.ajax({
            url: `/api/goals/${goalId}/achievement`,
            method: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify({ achievement_rate: rate, achievement_note: note }),
            success: function (res) {
                // 목표 목록 쪽의 해당 항목에도 달성률 반영
                const $goalLi = $(`.goal-item[data-id="${goalId}"]`);
                $goalLi.find('.achievement-display').remove();
                $goalLi.append(`<span class="achievement-display"> - 달성률 ${res.achievement_rate}% / ${res.achievement_note}</span>`);
                alert('저장되었습니다');
            },
            error: function (xhr) {
            alert(xhr.responseJSON.error);
            }
        });
    });
});
