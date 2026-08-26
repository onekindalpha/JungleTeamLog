$(function () {
  const teamPageId = $('#team-page-id').val();

  // 등록
  $('#coretime-register-btn').on('click', function () {
    const problem = $('#coretime-problem-input').val().trim();
    const solution = $('#coretime-solution-input').val().trim();

    if (!problem || !solution) {
      alert('문제와 해결 방법을 모두 입력해주세요');
      return;
    }

    $.ajax({
      url: `/api/team_pages/${teamPageId}/coretime`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ problem: problem, solution: solution }),
      success: function (res) {
        const c = res.coretime;
        const html = `
          <li class="coretime-item" data-id="${c._id}">
            <span class="coretime-date">${c.log_date}</span>
            <span class="coretime-name">${c.user_name}</span>
            <button class="coretime-edit-btn">수정</button>
            <button class="coretime-delete-btn">삭제</button>
            <br>
            <span>문제:</span> <span class="coretime-problem">${c.problem}</span><br>
            <span>해결:</span> <span class="coretime-solution">${c.solution}</span>
          </li>
        `;
        $('#coretime-list').prepend(html);
        $('#coretime-problem-input').val('');
        $('#coretime-solution-input').val('');
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });

  // 더보기
  $('#coretime-more-btn').on('click', function () {
    $('.coretime-hidden').removeClass('coretime-hidden');
    $(this).hide();
  });

  // 수정 버튼 → 인라인 입력창 전환
  $('#coretime-list').on('click', '.coretime-edit-btn', function () {
    const $li = $(this).closest('.coretime-item');
    const currentProblem = $li.find('.coretime-problem').text();
    const currentSolution = $li.find('.coretime-solution').text();

    $li.find('.coretime-problem').replaceWith(
      `<input type="text" class="coretime-edit-problem" value="${currentProblem}">`
    );
    $li.find('.coretime-solution').replaceWith(
      `<input type="text" class="coretime-edit-solution" value="${currentSolution}">`
    );
    $(this).text('저장').removeClass('coretime-edit-btn').addClass('coretime-save-btn');
  });

  // 저장
  $('#coretime-list').on('click', '.coretime-save-btn', function () {
    const $li = $(this).closest('.coretime-item');
    const coretimeId = $li.data('id');
    const newProblem = $li.find('.coretime-edit-problem').val().trim();
    const newSolution = $li.find('.coretime-edit-solution').val().trim();

    if (!newProblem || !newSolution) {
      alert('문제와 해결 방법을 모두 입력해주세요');
      return;
    }

    $.ajax({
      url: `/api/coretime/${coretimeId}`,
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({ problem: newProblem, solution: newSolution }),
      success: function (res) {
        $li.find('.coretime-edit-problem').replaceWith(`<span class="coretime-problem">${res.problem}</span>`);
        $li.find('.coretime-edit-solution').replaceWith(`<span class="coretime-solution">${res.solution}</span>`);
        $li.find('.coretime-save-btn').text('수정').removeClass('coretime-save-btn').addClass('coretime-edit-btn');
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });

  // 삭제
  $('#coretime-list').on('click', '.coretime-delete-btn', function () {
    const $li = $(this).closest('.coretime-item');
    const coretimeId = $li.data('id');

    if (!confirm('삭제하시겠습니까?')) return;

    $.ajax({
      url: `/api/coretime/${coretimeId}`,
      method: 'DELETE',
      success: function () {
        $li.remove();
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });
});