document.addEventListener('DOMContentLoaded', (event) => {
    const texts = ["EMPOWER", "FASHION", "STYLE", "UNIQUE", "GROWTH"];
    let index = 0;
    const changeText = () => {
        const textElement = document.getElementById('changingText');
        textElement.textContent = texts[index];
        index = (index + 1) % texts.length;
    };
    changeText();
    setInterval(changeText, 800); // Change text every 0.8 seconds
});


document.addEventListener("DOMContentLoaded", function() {
    const page3 = document.getElementById("page3");
    const leftSection = page3.querySelector(".left-section");
    const rightSection = page3.querySelector(".right-section");

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                leftSection.classList.add("show");
                rightSection.classList.add("show");
            } else {
                leftSection.classList.remove("show");
                rightSection.classList.remove("show");
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    observer.observe(page3);

    // Add click event listeners for each figure
    const figures = page3.querySelectorAll("figure");
    figures.forEach(figure => {
        figure.addEventListener("click", () => {
            figure.classList.toggle("active");
        });
    });
});

document.getElementById('contactButton').addEventListener('click', function() {
    document.getElementById('contactSection').scrollIntoView({ behavior: 'smooth' });
});

window.addEventListener('scroll', function() {
    const headerRight = document.querySelector('.header-right');
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    // Calculate the percentage of the page that has been scrolled
    const scrollPercentage = scrollY / maxScroll;

    // Calculate the new width based on the scroll percentage
    const minWidth = 205; // Initial width in pixels
    const maxWidth = window.innerWidth; // Full width
    const newWidth = minWidth + (maxWidth - minWidth) * scrollPercentage;

    // Set the new width of the header-right
    headerRight.style.width = `${newWidth}px`;
});


//------------------------SIDE BAR---------------------------//

function openNav() {
    document.getElementById("mySidebar").style.width = "1000px";
    document.getElementById("overlay").style.display = "block";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("overlay").style.display = "none";
}

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





