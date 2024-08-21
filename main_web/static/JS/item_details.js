document.addEventListener('DOMContentLoaded', function() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.querySelector('.main-image img');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const newSrc = this.src;
            mainImage.src = newSrc;
        });
    });
});



document.querySelector('.custom-select').addEventListener('click', function() {
    this.classList.toggle('active');
    const options = this.nextElementSibling;
    if (options.style.display === 'block') {
        options.style.display = 'none';
    } else {
        options.style.display = 'block';
    }
});

document.querySelectorAll('.custom-options li').forEach(option => {
    option.addEventListener('click', function() {
        const select = this.closest('.custom-select-container').querySelector('.custom-select span');
        select.textContent = this.textContent;
        const options = this.closest('.custom-options');
        options.style.display = 'none';
        options.previousElementSibling.classList.remove('active');
    });
});


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
//make images bigger 

function openModal(element) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    modal.style.display = "block";
    modalImg.src = element.src;
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = "none";
}
