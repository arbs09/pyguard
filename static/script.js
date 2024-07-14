$(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault();
        var query = $('#query').val();
        fetchSearchResults(query);
    });

    function fetchSearchResults(query) {
        $.ajax({
            url: '/search',
            type: 'GET',
            data: { query: query },
            success: function(response) {
                displaySearchResults(response);
            },
            error: function(error) {
                console.error('Error fetching search results:', error);
            }
        });
    }

    function displaySearchResults(results) {
        $('#search-results').empty();
        if (results.length > 0) {
            $('#search-results').show();
            results.forEach(function(result) {
                for (const [key, value] of Object.entries(result)) {
                    $('#search-results').append(`
                        <li class="list-group-item py-2">
                            <h6 class="mb-1">${value.name}</h6>
                            <div class="small">
                                <p class="mb-1"><strong>ID:</strong> ${key}</p>
                                <p class="mb-1"><strong>Level:</strong> ${value.level}</p>
                                <p class="mb-1"><strong>XP:</strong> ${value.xp}</p>
                                <p class="mb-1"><strong>First Time Logged:</strong> ${value.first_login}</p>
                                <p class="mb-1"><strong>Last Time Logged:</strong> ${value.last_login}</p>
                            </div>
                        </li>
                    `);
                }
            });
        } else {
            $('#search-results').hide();
        }
    }

    function fetchTop10ByXP() {
        $.ajax({
            url: '/top10xp',
            type: 'GET',
            success: function(response) {
                displayTop10ByXP(response);
            },
            error: function(error) {
                console.error('Error fetching top 10 by XP:', error);
            }
        });
    }

    function displayTop10ByXP(users) {
        $('#top-10-by-xp').empty();
        if (users.length > 0) {
            users.forEach(function(user, index) {
                if (index < 3) {
                    $('#top-10-by-xp').append(`
                        <li class="list-group-item list-group-item-primary py-2">
                            <h6 class="mb-1">${index + 1}. Rank</h6>
                            <p class="small mb-1">${user.name} (ID: ${user.id}) - XP: ${user.xp}</p>
                        </li>
                    `);
                } else {
                    $('#top-10-by-xp').append(`
                        <li class="list-group-item py-2">
                            <p class="small mb-1">${user.name} (ID: ${user.id}) - XP: ${user.xp}</p>
                        </li>
                    `);
                }
            });
        } else {
            $('#top-10-by-xp').append('<li class="list-group-item py-2">No users found</li>');
        }
    }

    // Initial fetch of top 10 users by XP
    fetchTop10ByXP();
    // Refresh top 10 users by XP every 60 seconds
    setInterval(fetchTop10ByXP, 60000);
});
