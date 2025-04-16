window.onload = () => {
    // Get the stored token from localStorage
    const token = localStorage.getItem('authToken');

    if (!token) {
        alert('Please log in first.');
        window.location.href = 'login.html'; // Redirect to login if no token
        return;
    }

    // Use token to fetch user listings and name
    fetch('http://127.0.0.1:5000/account_listings', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show user name
            document.getElementById('user-name-heading').textContent = `Welcome, ${data.name}!`;

            // Populate listings
            const listingsDiv = document.getElementById('user-listings');
            if (data.listings && data.listings.length > 0) {
                data.listings.forEach(listing => {
                    const listingDiv = document.createElement('div');
                    listingDiv.innerHTML = `
                        <p><strong>Book Name:</strong> ${listing.l_bookname}</p>
                        <p><strong>Condition:</strong> ${listing.l_condition}</p>
                        <p><strong>Price:</strong> $${listing.l_price}</p>
                        <button class="remove-listing-btn" data-id="${listing.l_id}">Remove Listing</button>
                    `;
                    listingsDiv.appendChild(listingDiv);
                });
            } else {
                listingsDiv.innerHTML = "<p>No listings found.</p>";
            }
        } else {
            alert('Failed to load account data: ' + data.message);
        }
    })    
    .catch(err => {
        console.error('Error fetching user listings:', err);
        alert('An error occurred while fetching your listings.');
    });

    // Show create listing form
    document.getElementById('create-listing-btn').addEventListener('click', () => {
        document.getElementById('create-listing-form').style.display = 'block';
    });

    // Handle listing creation
    document.getElementById('submit-listing-btn').addEventListener('click', () => {
        const bookName = document.getElementById('book-name').value;
        const bookCondition = document.getElementById('book-condition').value;
        const bookPrice = document.getElementById('book-price').value;

        if (!bookName || !bookCondition || !bookPrice) {
            alert('Please fill in all fields.');
            return;
        }

        // Send POST request to create new listing
        fetch('http://127.0.0.1:5000/create_listing', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                l_bookname: bookName,
                l_condition: bookCondition,
                l_price: bookPrice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Listing created successfully.');
                location.reload(); // Reload page to show new listing
            } else {
                alert('Error creating listing.');
            }
        })
        .catch(err => {
            console.error('Error creating listing:', err);
            alert('An error occurred while creating the listing.');
        });
    });

    // Handle listing removal
    document.getElementById('user-listings').addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-listing-btn')) {
            const listingId = e.target.getAttribute('data-id');
            fetch(`http://127.0.0.1:5000/remove_listing/${listingId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Listing removed successfully.');
                    location.reload(); // Reload page to update listings
                } else {
                    alert('Error removing listing.');
                }
            })
            .catch(err => {
                console.error('Error removing listing:', err);
                alert('An error occurred while removing the listing.');
            });
        }
    });

    // Handle logout
    document.getElementById('logout-btn').addEventListener('click', () => {
        // Clear token from localStorage
        localStorage.removeItem('authToken');

        // Send logout request to server
        fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Successfully logged out.');
                window.location.href = 'index.html'; // Redirect to home page after logout
            } else {
                alert('Error during logout.');
            }
        })
        .catch(err => {
            console.error('Error during logout:', err);
            alert('An error occurred while logging out.');
        });
    });
};
