

document.addEventListener('DOMContentLoaded', () => {
    const bubbleContainer = document.querySelector('.bubble-container');
    const totalBubbles = 20;
    const tripleBubbles = totalBubbles / 4;

    for (let i = 0; i < totalBubbles; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.classList.add(i < tripleBubbles ? 'green' : i < 2*tripleBubbles ? 'pink':i< 3*tripleBubbles?'blue':'yellow');
        const size = Math.random() * 60 + 20;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${Math.random() * 100}%`;
        bubble.style.animationDuration = `${Math.random() * 5 + 3}s`;
        bubbleContainer.appendChild(bubble);
    }
});