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
          <li class="coretime-item box py-3 px-4 mb-2" data-id="${c._id}">
            <span class="coretime-date tag is-light"></span>
            <span class="coretime-name has-text-weight-semibold ml-2"></span>
            <div class="buttons is-pulled-right">
              <button class="coretime-edit-btn button is-small is-link is-light">수정</button>
              <button class="coretime-delete-btn button is-small is-danger is-light">삭제</button>
            </div>
            <br>
            <p class="mt-2"><strong>문제:</strong> <span class="coretime-problem"></span></p>
            <p><strong>해결:</strong> <span class="coretime-solution"></span></p>
          </li>
        `;
        const $li = $(html);
        // XSS 방지: text()로 안전하게 값 삽입
        $li.find('.coretime-date').text(c.log_date);
        $li.find('.coretime-name').text(c.user_name);
        $li.find('.coretime-problem').text(c.problem);
        $li.find('.coretime-solution').text(c.solution);

        $('#coretime-list').prepend($li);
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

    const $problemInput = $('<input type="text" class="coretime-edit-problem input is-small">').val(currentProblem);
    const $solutionInput = $('<input type="text" class="coretime-edit-solution input is-small">').val(currentSolution);

    $li.find('.coretime-problem').replaceWith($problemInput);
    $li.find('.coretime-solution').replaceWith($solutionInput);

    $(this).text('저장')
      .removeClass('coretime-edit-btn is-link is-light')
      .addClass('coretime-save-btn is-primary');
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
        const $problemSpan = $('<span class="coretime-problem"></span>').text(res.problem);
        const $solutionSpan = $('<span class="coretime-solution"></span>').text(res.solution);

        $li.find('.coretime-edit-problem').replaceWith($problemSpan);
        $li.find('.coretime-edit-solution').replaceWith($solutionSpan);

        $li.find('.coretime-save-btn').text('수정')
          .removeClass('coretime-save-btn is-primary')
          .addClass('coretime-edit-btn is-link is-light');
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