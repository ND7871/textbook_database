document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get("query") || "";

    const listingsContainer = document.getElementById("listings");

    fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(searchQuery)}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                listingsContainer.innerHTML = data
                    .map((listing) => {
                        return `
                            <div class="listing">
                                <h3>${listing.t_name}</h3>
                                <p><strong>Class:</strong> ${listing.t_class}</p>
                                <p><strong>Professor:</strong> ${listing.t_professor || "N/A"}</p>
                                <p><strong>Required:</strong> ${listing.t_required ? "Yes" : "No"}</p>
                                <a href="textbook.html?id=${encodeURIComponent(listing.t_name)}">View Details</a>
                            </div>
                        `;
                    })
                    .join("");
            } else{
                listingsContainer.innerHTML = `<p>No results found for "${searchQuery}".</p>`;
            }
    })
    .catch((error) => {
        console.error("Error fetching search results:", error);
        listingsContainer.innerHTML = "<p>Error loading listings.</p>";
    });
});
