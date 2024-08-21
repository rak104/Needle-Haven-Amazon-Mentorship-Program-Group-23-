// Function to open the sidebar
function openNav() {
    document.getElementById("mySidebar").style.width = "1000px";
    document.getElementById("overlay").style.display = "block";
}

// Function to close the sidebar
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("overlay").style.display = "none";
}

// Function to show the selected tab in the sidebar
function showTab(tab) {
    document.getElementById('items-tab').classList.remove('active');
    document.getElementById('stores-tab').classList.remove('active');
    document.getElementById(tab + '-tab').classList.add('active');
}

// Close the sidebar if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById("overlay")) {
        closeNav();
    }
}


window.onload = function() {

    // Ensure the sidebar is open if it was open before
    if ("{{ sidebar_open }}" === "True") {
        document.getElementById("mySidebar").style.width = "50vw"; // Set sidebar width to half the viewport width
        document.getElementById("overlay").style.display = "block";
    }

};

function selectTab(tabName) {
    document.getElementById('selectedTab').value = tabName;

    const itemsTab = document.getElementById('items-tab');
    const storesTab = document.getElementById('stores-tab');

    if (tabName === 'items') {
        itemsTab.classList.add('active');
        storesTab.classList.remove('active');
    } else if (tabName === 'stores') {
        storesTab.classList.add('active');
        itemsTab.classList.remove('active');
    }
}



document.addEventListener('DOMContentLoaded', () => {
    const sortByButton = document.querySelector('.sort-by-button');
    const sortOptions = document.querySelector('.sort-options');

    // Toggle the display of sort options when the sort button is clicked
    sortByButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent the event from bubbling up to the window
        sortOptions.style.display = sortOptions.style.display === 'block' ? 'none' : 'block';
    });

    // Close the sort options when clicking outside of the sort options
    window.addEventListener('click', (event) => {
        if (!sortByButton.contains(event.target) && !sortOptions.contains(event.target)) {
            sortOptions.style.display = 'none';
        }
    });

    // Handle the sort option click event
    sortOptions.querySelectorAll('a').forEach(option => {
        option.addEventListener('click', (event) => {
            event.preventDefault();
            const sortType = event.target.getAttribute('data-sort');

            // Redirect to the backend with the sort type
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('sort', sortType);
            window.location.href = currentUrl.toString();
        });
    });
});
