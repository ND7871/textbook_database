document.getElementById('search-btn').addEventListener('click', () => {
    const isbn = document.getElementById('isbn-input').value;
    fetch('/search?query=${isbn}')
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
});

const displayResults = (data) => {
    const offerContainer = document.getElementById('offer-container');
    offerContainer.innerHTML = '';
    if (data.length > 0) {
        data.forEach(book => {
            offerContainer.innerHTML += <div>
                <h3>${book[0]}</h3>
                <p>Class: ${book[1]}</p>
                <p>Professor: ${book[2]}</p>
                <p>eBook: ${book[3] ? 'Yes' : 'No'}</p>
                <p>Required: ${book[4] ? 'Yes' : 'No'}</p>
                <p>Link: <a href="${book[5]}" target="_blank">${book[5]}</a></p>
            </div>;
        });
    } else {
        offerContainer.innerHTML = '<p>No results found.</p>';
    }
};
