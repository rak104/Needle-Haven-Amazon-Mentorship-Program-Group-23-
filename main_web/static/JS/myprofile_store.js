function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');
    selectedSection.style.display = 'block';
}

document.addEventListener('click', function(event) {
    const sidebar = document.querySelector('.left-sidebar');
    const menuButton = document.querySelector('.navbar-button i');

    if (!sidebar.contains(event.target) && !menuButton.contains(event.target)) {
        sidebar.classList.remove('open');
        document.querySelector('.main-container').classList.remove('shift');
    }
});

function toggleChangePasswordForm() {
    const form = document.getElementById('change-password-form');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}

// Initially hide all sections except the active one (store-info)
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.section').forEach(section => {
        if (!section.classList.contains('active')) {
            section.style.display = 'none';
        }
    });
});

function toggleMenu() {
    const menu = document.getElementById('menuDropdown');
    menu.classList.toggle('show');
}

function handleImageUpload(input) {
    const photoBox = input.closest('.photo-box');
    const imgElement = photoBox.querySelector('.preview-img');
    const deleteBtn = photoBox.querySelector('.delete-btn');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imgElement.src = e.target.result;
            imgElement.style.display = 'block';
            deleteBtn.style.display = 'block';
            photoBox.querySelector('span').style.display = 'none';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function deleteImage(button) {
    const photoBox = button.closest('.photo-box');
    const imgElement = photoBox.querySelector('.preview-img');
    const fileInput = photoBox.querySelector('.file-input');

    imgElement.src = '';
    imgElement.style.display = 'none';
    button.style.display = 'none';
    photoBox.querySelector('span').style.display = 'block';
    fileInput.value = ''; // Clear the file input
}

// Initialize the current step
let currentStep = 1;

function showStep(stepNumber) {
    // Hide all step sections
    document.querySelectorAll('.step-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected step section based on the step number
    const stepSection = document.getElementById(`step-${stepNumber}`);
    if (stepSection) {
        stepSection.style.display = 'block';
    }

    // Update active step indicator
    document.querySelectorAll('.step').forEach((step, index) => {
        if (index < stepNumber) {
            step.classList.add('completed');
            step.style.opacity = '1'; // Fully visible for completed steps
            step.style.pointerEvents = 'auto'; // Clickable
        } else if (index === stepNumber - 1) {
            step.classList.add('active');
            step.style.opacity = '1'; // Fully visible for active steps
            step.style.pointerEvents = 'auto'; // Clickable
        } else {
            step.classList.remove('completed');
            step.classList.remove('active');
            step.style.opacity = '0.5'; // Fade effect for inactive steps
            step.style.pointerEvents = 'none'; // Not clickable
        }
    });
}


// Move to the next step (Photo Upload)
document.getElementById('nextToPhotoUpload').addEventListener('click', function () {
    currentStep = 2;
    showStep(currentStep);
    document.querySelector('.item-details-form').style.display = 'none'; // Hide item details
    document.getElementById('step-upload-photo').style.display = 'block'; // Show photo upload
});

// Move to the next step (Review)
document.getElementById('nextToReview').addEventListener('click', function () {
    currentStep = 3;
    showStep(currentStep);
    document.getElementById('step-upload-photo').style.display = 'none'; // Hide photo upload
    document.getElementById('step-review').style.display = 'block'; // Show review step
});

// Move to the previous step (Photo Upload)
document.getElementById('backToUpload').addEventListener('click', function () {
    currentStep = 2;
    showStep(currentStep);
    document.getElementById('step-review').style.display = 'none'; // Hide review step
    document.getElementById('step-upload-photo').style.display = 'block'; // Show photo upload step
});

// Move to the previous step (Item Details)
document.getElementById('backToDetails').addEventListener('click', function () {
    currentStep = 1;
    showStep(currentStep);
    document.getElementById('step-upload-photo').style.display = 'none'; // Hide review step
    document.getElementById('step-item-details').style.display = 'block'; // Show photo upload step
});

// Event listener to close the menu when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('menuDropdown');
    const menuButton = document.querySelector('.navbar-button');

    if (!menu.contains(event.target) && !menuButton.contains(event.target)) {
        menu.classList.remove('show');
    }
});


const typeAndSizeOptions = {
    Menswear: {
        Clothing: {
            types: ['T-Shirts & Polos', 'Shirts', 'Sweaters & Hoodies', 
            'Jackets & Coats', 'Suits & Blazers', 'Pants & Chinos', 
            'Jeans', 'Shorts', 'Activewear', 'Swimwear'],
            sizes: ['S', 'M', 'L', 'XL', 'XXL','XXXL']
        },
        Shoes: {
            types: ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals'],
            sizes: ['39', '40', '41', '42', '43', '44', '45','46','47','48','49']
        },
        Accessories: {
            types: ['Bags', 'Belts', 'Hats', 'Watches', 'Sunglasses'],
            sizes: ['One Size']
        }
    },
    Womenswear: {
        Clothing: {
            types: ['Dresses',
            'Tops & Blouses',
            'T-shirts & Tanks',
            'Sweaters & Cardigans',
            'Jackets & Coats',
            'Pants & Leggings',
            'Skirts',
            'Shorts',
            'Jeans',
            'Suits & Blazers',
            'Activewear',
            'Swimwear'],
            sizes: ['XS', 'S', 'M', 'L', 'XL']
        },
        Shoes: {
            types: ['Heels', 'Flats', 'Boots', 'Sneakers', 'Sandals'],
            sizes: ['33', '34', '35', '36', '37', '38','39','40']
        },
        Accessories: {
            types: ['Bags', 'Belts', 'Hats', 'Jewelry', 'Scarves'],
            sizes: ['One Size']
        }
    },
    Kidswear: {
        Clothing: {
            types: ['Tops', 'Pants', 'Dresses', 'Outerwear', 'Swimwear'],
            sizes: ['XS','S', 'M', 'L', 'XL', 'XXL','XXXL']
        },
        Shoes: {
            types: ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals'],
            sizes:['20', '21', '22', '23', '24', '25','26','27','28','29','30','31','32','33', '34', '35', '36', '37', '38']
        },
        Accessories: {
            types: ['Hats', 'Bags', 'Scarves', 'Gloves'],
            sizes: ['One Size']
        }
    }
};

function updateTypesAndSizes() {
    const category = document.getElementById('category').value;
    const subcategory = document.getElementById('subcategory').value;
    const typeSelect = document.getElementById('type');
    const sizeSelect = document.getElementById('size');

    typeSelect.innerHTML = ''; // Clear current type options
    sizeSelect.innerHTML = ''; // Clear current size options

    if (typeAndSizeOptions[category] && typeAndSizeOptions[category][subcategory]) {
        const options = typeAndSizeOptions[category][subcategory];

        // Populate type options
        options.types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeSelect.appendChild(option);
        });

        // Populate size options
        options.sizes.forEach(size => {
            const option = document.createElement('option');
            option.value = size;
            option.textContent = size;
            sizeSelect.appendChild(option);
        });
    }
}

// Add event listeners to update types and sizes when category or subcategory changes
document.getElementById('category').addEventListener('change', updateTypesAndSizes);
document.getElementById('subcategory').addEventListener('change', updateTypesAndSizes);


// Populate the review section
document.getElementById('nextToReview').addEventListener('click', function () {
    document.getElementById('review-item-name').textContent = document.getElementById('item-name').value;
    document.getElementById('review-category').textContent = document.getElementById('category').value;
    document.getElementById('review-subcategory').textContent = document.getElementById('subcategory').value;
    document.getElementById('review-type').textContent = document.getElementById('type').value;
    document.getElementById('review-size').textContent = document.getElementById('size').value;
    document.getElementById('review-color').textContent = document.getElementById('color').value;
    document.getElementById('review-description').textContent = document.getElementById('description').value;
    document.getElementById('review-price').textContent = document.getElementById('price').value;

    const reviewImagesContainer = document.getElementById('review-images');
    reviewImagesContainer.innerHTML = '';
    document.querySelectorAll('.photo-box .preview-img').forEach(function(img) {
        if (img.src) {
            const imgElement = document.createElement('img');
            imgElement.src = img.src;
            reviewImagesContainer.appendChild(imgElement);
        }
    });
});


document.querySelector('.submit-button').addEventListener('click', function(event) {
    // Fetch all fields to validate
    const itemName = document.getElementById('review-item-name').textContent.trim();
    const category = document.getElementById('review-category').textContent.trim();
    const subcategory = document.getElementById('review-subcategory').textContent.trim();
    const type = document.getElementById('review-type').textContent.trim();
    const size = document.getElementById('review-size').textContent.trim();
    const color = document.getElementById('review-color').textContent.trim();
    const description = document.getElementById('review-description').textContent.trim();
    const price = document.getElementById('review-price').textContent.trim();

    // Check if any field is empty
    let isFormValid = true;
    
    if (!itemName || !category || !subcategory || !type || !size || !color || !description || !price) {
        isFormValid = false;
    }

    // Check if photos are uploaded
    const photoBoxes = document.querySelectorAll('.photo-box');
    let arePhotosUploaded = true;

    photoBoxes.forEach(box => {
        const imgElement = box.querySelector('.preview-img');
        if (!imgElement || imgElement.src === "") {
            arePhotosUploaded = false;
        }
    });

    if (!arePhotosUploaded) {
        isFormValid = false;
    }

    if (!isFormValid) {
        event.preventDefault(); // Prevent form submission
        document.getElementById('error-message').style.display = 'block'; // Show error message
        document.getElementById('error-message').textContent = 'Please fill out all required fields and upload all required photos.';
    } else {
        document.getElementById('error-message').style.display = 'none'; // Hide error message
        // Optionally, you can submit the form here or continue with your logic
    }
});


document.getElementById('productForm').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        // Optionally, you can trigger a click on the "Next" button
        document.getElementById('nextToPhotoUpload').click();
    }
});
