document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('slider');
    const popup = document.getElementById('popup');
    const buttons = popup.querySelectorAll('.close, .sell-button');
    const fire = popup.querySelector('.fire');
    const textContainer = popup.querySelector('.text');

    let animationStopped = false;
    let selectedItems = [];
    let totalSpins = 1;
    let currentSpin = 0;

    const persistSpin = localStorage.getItem('persistSpinChecked') === 'true';
    const quickSpin = localStorage.getItem('quickSpinChecked') === 'true';

    // Set the checkbox state based on localStorage value
    if (persistSpin) {
        $('#persist-spin-checkbox').prop('checked', true);
    }

    // Handle the checkbox state change
    $('#persist-spin-checkbox').change(function () {
        localStorage.setItem('persistSpinChecked', $(this).prop('checked').toString());
    });

    $('#quickspin-checkbox').change(function () {
        localStorage.setItem('quickSpinChecked', $(this).prop('checked').toString());
    });

    // Update total spins when a spin option is clicked
    $(".spin-option").click(function () {
        $(".spin-option").removeClass("selected");

        // Play sound bubble_selection.mp3
        let audio = new Audio("/static/css/sounds/bubble_selection.mp3");
        audio.play();

        $(this).addClass("selected");
        totalSpins = parseInt($(this).data("value"));
        sessionStorage.setItem("totalSpins", totalSpins);
    });


    // Start animation on button click
    $(".start").click(function (event) {
        const buttonId = event.target.id; // Extract the ID of the clicked button
        console.log(`Button clicked: ${buttonId}`); // Debug: Log the button's ID
        sessionStorage.setItem("startAnimation", "true");
        sessionStorage.setItem("isQuickSpin", $("#quickspin-checkbox").is(":checked"));

        // Reset current spin count and initialize the animation


        let currentSpin = 0;
        console.log('current spin set to 0')
        initializeAnimation(buttonId);
    });

    function initializeAnimation(buttonId) {
        $(".start").prop('disabled', true);
        const isQuickSpin = sessionStorage.getItem("isQuickSpin") === "true";
        selectedItems = [];
        console.log(`Initializing animation for button: ${buttonId}`); // Debug log for button ID



async function randomizeContents() {
    const startButton = document.getElementById("start");
    const gameId = startButton.getAttribute("data-game-id");
    const nonce = startButton.getAttribute("data-nonce");
    const slug = startButton.getAttribute("data-slug");

    console.log("Game ID:", gameId);
    console.log("Nonce:", nonce);
    console.log("Slug:", slug);

    try {
        const payload = { game_id: gameId };
        console.log("Payload sent to server:", payload);

        // Call the create_outcome endpoint
        const response = await fetch(`/create_outcome/${slug}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        console.log("Response from server:", data);

        if (data.status === 'success') {
            startButton.setAttribute('data-nonce', data.nonce);
            console.log(`Nonce updated: ${data.nonce}`);

            // Clear existing cards
            clearCards();

            const attributes = {
                id: data.choice_id || 'N/A',
                nonce: data.nonce || 'N/A',
                text: data.choice_text || 'Unknown',
                color: data.choice_color || '#FFFFFF',
                file: data.choice_file || null,
                value: data.choice_value || 0,
                lowerNonce: data.lower_nonce || 'N/A',
                upperNonce: data.upper_nonce || 'N/A',
            };

            const targetCardElement = document.createElement('div');
            targetCardElement.classList.add('card', 'target-card');
            targetCardElement.setAttribute('id', `card-${attributes.id}`);
            targetCardElement.setAttribute('data-nonce', attributes.nonce);
            targetCardElement.setAttribute('data-color', attributes.color);
            targetCardElement.setAttribute('data-choice_value', attributes.value);
            targetCardElement.setAttribute('data-lower_nonce', attributes.lowerNonce);
            targetCardElement.setAttribute('data-upper_nonce', attributes.upperNonce);

            targetCardElement.innerHTML = `
    <div class="cards" style="background: url(/static/css/images/${attributes.color}.png);">
            <div class="lootelement"
     data-price="${attributes.value || ''}"
     data-currency-file="${attributes.currencyFile || ''}"
     data-currency-symbol="${attributes.currencySymbol || ''}"
     style="display: flex; flex-direction: column; align-items: center; height: 100%; align-self: flex-start; border: 0.1em solid grey; border-top: none; width: 10em;">
    ${attributes.file ? `<div class="sliderImg" style="background-image: url(${attributes.file}); background-repeat: no-repeat; background-position: center; background-size: contain; height: 10em; width: 100%;"></div>` : ''}
    <div class="sliderPrice">${attributes.value} 💎</div>
</div>
</div>
`;

            selectedItems.push({
                id: attributes.id,
                nonce: attributes.nonce,
                text: attributes.text,
                color: attributes.color,
                src: attributes.file,
                value: attributes.value,
                lowerNonce: attributes.lowerNonce,
                upperNonce: attributes.upperNonce
            });

            const cardContainer = document.querySelector('.slider'); // Adjust selector if necessary

            // Calculate the position to insert: 4 cards to the right of the middle
            const middleIndex = Math.floor(cardContainer.children.length / 2);
            const targetIndex = Math.min(
                cardContainer.children.length,
                middleIndex + 4
            );

            if (cardContainer.children[targetIndex]) {
                cardContainer.insertBefore(targetCardElement, cardContainer.children[targetIndex]);
            } else {
                cardContainer.appendChild(targetCardElement);
            }

            console.log("Target card inserted 4 cards to the right of the middle.");

            // Call create_inventory_object after the card is created
            const inventoryPayload = {
                choice_id: data.choice_id, // Use choice_id from outcome response
                choice_value: data.choice_value, // Use choice_value
                category: data.category, // Additional data as needed
                price: 100,
                condition: 'New',
                quantity: 1,
                buttonId: buttonId,
            };
            console.log("Calling /create_inventory_object/ with payload:", inventoryPayload);

            const inventoryResponse = await fetch('/create_inventory_object/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}', // Ensure CSRF token is correctly passed
                },
                body: JSON.stringify(inventoryPayload),
            });

            const inventoryData = await inventoryResponse.json();
            console.log("Response from /create_inventory_object/:", inventoryData);

            if (inventoryData.status === 'success') {
                if (inventoryData.button_id === "start") {
                    console.log("Inventory object created successfully with user.");
                     let inventory_pk = inventoryData.inventory_object_id;
                        console.log("inventory_pk:", inventory_pk);
                        inventory_pk = inventory_pk;
                        targetCardElement.setAttribute('data-inventory_pk', window.inventory_pk);

                        window.sellUrl = `/inventory/${inventory_pk}/sell/`;
                        const sellForm = document.getElementById(`sell-form-${window.inventory_pk}`);
                        console.log('sellform: ' + sellForm);
                        if (sellForm) {
                          console.log("Sell form found:", sellForm);

                          sellForm.addEventListener('submit', function(event) {
                            event.preventDefault();
                            const pk = this.querySelector('[name="pk"]').value;
                            console.log("Sell form submitted. pk =", pk);

                            $(".spin-option").removeClass("selected");


                            $(this).addClass("selected");
                            totalSpins = parseInt($(this).data("value"));
                            sessionStorage.setItem("totalSpins", totalSpins);
                            sellInventory(pk);
                          });
                        } else {
                          console.error("Sell form not found for inventory_pk:", window.inventory_pk);
                        }

                } else if (inventoryData.button_id === "start2") {
                    console.log("Temporary inventory object created without user. ID:", inventoryData.inventory_object_id);
                }
            } else {
                console.error("Failed to create inventory object:", inventoryData.message);
            }

            return data;
        } else {
            console.error(`Error: ${data.message}`);
            return null;
        }
    } catch (error) {
        console.error(`Request failed: ${error}`);
        return null;
    }
}


function clearCards() {
    const cardContainer = document.querySelector('.slider');
    const targetCards = cardContainer.querySelectorAll('.target-card');

    targetCards.forEach(card => cardContainer.removeChild(card));

    console.log("All target cards removed.");
}

// Function to center the card in the slider
function centerCard(cardElement) {
    const slider = document.getElementById('slider');
    const cardOffset = cardElement.offsetLeft;
    const sliderWidth = slider.offsetWidth;
    const cardWidth = cardElement.offsetWidth;

    // Adjust margin-left to center the card
    slider.scrollTo({
        left: cardOffset - sliderWidth / 2 + cardWidth / 2,
        behavior: 'smooth',
    });
}



        function addAnimation() {
            document.querySelectorAll('.slider').forEach(scroller => {
                scroller.style.animation = 'none';
                scroller.offsetHeight;  // Trigger reflow
                let animationDuration = isQuickSpin ? '9s' : '18s';
                scroller.style.animation = `slideshow ${animationDuration} cubic-bezier(0.25, 0.1, 0.25, 1) forwards`;
                scroller.style.animationPlayState = 'running';
            });
        }

function alignCardWithSpinner() {
    const spinnerTick = document.getElementById('selector'); // The spinner tick element
    const slider = document.getElementById('slider');
    const targetCard = document.querySelector('.target-card'); // The new card to align

    if (!targetCard || !spinnerTick) {
        console.error('Target card or spinner tick not found!');
        return;
    }

    // Get the center position of the spinner tick
    const spinnerTickRect = spinnerTick.getBoundingClientRect();
    const spinnerTickCenter = spinnerTickRect.left + spinnerTickRect.width / 2;

    // Get the center position of the target card
    const targetCardRect = targetCard.getBoundingClientRect();
    const targetCardCenter = targetCardRect.left + targetCardRect.width / 2;

    // Calculate the offset needed to align the card with the spinner tick
    const offset = spinnerTickCenter - targetCardCenter;

    // Update the slider's translateX value
    const currentTransform = getComputedStyle(slider).transform;
    const matrix = new DOMMatrix(currentTransform); // Use DOMMatrix for robust transformation parsing
    const currentTranslateX = matrix.m41 || 0;

    //slider.style.transform = `translateX(${currentTranslateX + offset}px)`;
    //console.log(`Slider adjusted by offset: ${offset}px`);
}



$(".start").click(function (event) {
    const buttonId = event.target.id; // Extract the ID of the clicked button
    console.log(`Button clicked: ${buttonId}`); // Debug: Log the button's ID

});


const casinoThump = new Audio('/static/css/sounds/thump.mp3');
const casinoGreen = new Audio('/static/css/sounds/money.mp3');
const casinoYellow = new Audio('/static/css/sounds/retro_video_game_col.mp3');
const casinoOrange = new Audio('/static/css/sounds/click-nice.mp3');
const casinoRed = new Audio('/static/css/sounds/redwin.mp3');
const casinoBlack = new Audio('/static/css/sounds/blackwin.mp3');
const casinoRedBlack = new Audio('/static/css/sounds/rap.mp3');
const casinoRedGold = new Audio('/static/css/sounds/ultimatewin.mp3');

function playThump() {
    casinoThump.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoGreenSound() {
    casinoGreen.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoYellowSound() {
    casinoYellow.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoOrangeSound() {
    casinoOrange.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoRedSound() {
    casinoRed.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoBlackSound() {
    casinoBlack.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoRedBlackSound() {
    casinoRedBlack.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function playCasinoRedGoldSound() {
    casinoRedGold.play().catch((error) => {
        console.error('Error playing casino-win audio:', error);
    });
}

function createTopHit(data) {
    fetch('/top-hits/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((result) => {
        if (result.error) {
            console.error('Error creating Top Hit:', result.error);
        } else {
            console.log('Top Hit created successfully:', result);
        }
    })
    .catch((error) => {
        console.error('Network error:', error);
    });
}


// Function to get CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;
}

// Select the target card
const targetCard = document.querySelector('.target-card');
let choiceColor = targetCard ? targetCard.getAttribute('data-color') : 'gray';

// Log and handle choiceColor
console.log('Given the choice color:', choiceColor);

function randomizedContents() {
    const slider = document.querySelector('.slider');
    const children = Array.from(slider.children);

    const targetIndex = children.findIndex(child => child.classList.contains('target-card'));
    let targetCard = null;
    if (targetIndex !== -1) {
        targetCard = children[targetIndex];
    }

    const nonTargetCards = children.filter(child => !child.classList.contains('target-card'));

    for (let i = nonTargetCards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [nonTargetCards[i], nonTargetCards[j]] = [nonTargetCards[j], nonTargetCards[i]];
    }

    slider.innerHTML = '';

    const totalCards = nonTargetCards.length + (targetCard ? 1 : 0);
    for (let i = 0, j = 0; i < totalCards; i++) {
        if (i === targetIndex && targetCard) {
            slider.appendChild(targetCard);
        } else {
            slider.appendChild(nonTargetCards[j]);
            j++;
        }
    }

    console.log("Slider contents randomized without affecting target card position.");
}



function spin(buttonId) {
    // Reset currentSpin to 0 when a button is pressed
    if (currentSpin === totalSpins || animationStopped) {
        currentSpin = 0; // Reset spin count
        animationStopped = false; // Ensure animations are not marked as stopped
    }

    $(".spin-option").prop('disabled', true);

    randomizeContents();
    randomizedContents();
    addAnimation();

    if (buttonId === "start") {
        console.log("Regular Spin triggered");
    } else if (buttonId === "start2") {
        console.log("Demo Spin triggered");
    }

    const animationDuration = isQuickSpin ? 4500 : 9000;
    const buffer = 150;
    const audiobuffer = 300;
    const audio = new Audio('/static/css/sounds/roulette_sound_effect.mp3');

    audio.addEventListener('loadedmetadata', () => {
        // Calculate the adjusted duration
        const adjustedDuration = (animationDuration + audiobuffer) / 1000; // Convert ms to seconds
        const originalDuration = audio.duration;

        if (originalDuration) {
            audio.playbackRate = originalDuration / adjustedDuration;
        }

        audio.play().catch((error) => console.error('Error playing audio:', error));
    });

    // Handle audio load errors
    audio.addEventListener('error', (e) => {
        console.error('Audio failed to load:', e);
    });

    // Call this function when the spin ends
setTimeout(() => {
    document.querySelectorAll('.slider').forEach((scroller) => {
        scroller.style.animationPlayState = 'paused';


    const targetCard = document.querySelector('.target-card'); // Find the target element

    const startButton = document.getElementById('start'); // Or use querySelector('.start')


    if (targetCard) {
        let choiceColor = targetCard.getAttribute('data-color') || 'gray';
        let choiceId = targetCard.getAttribute('id');
        let gameId = startButton.getAttribute("data-game-id");


        console.log('The choice color is:', choiceColor);
        console.log('The choice id is:', choiceId);
        console.log('The game id is:', gameId);
        if (choiceColor === 'gray') {
            playThump();

        } else if (choiceColor === 'green') {
            playCasinoGreenSound();
            $(".start").prop('disabled', true);
        } else if (choiceColor === 'yellow') {
                console.log('yellow hit')
            playCasinoGreenSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId, // Ensure this is set correctly
                };
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        } else if (choiceColor === 'orange') {
                console.log('orange hit')
            playCasinoYellowSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId,
                };
                // Create the Top Hit
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        } else if (choiceColor === 'red') {
                console.log('red hit')
            playCasinoRedSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId,
                };
                // Create the Top Hit
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        } else if (choiceColor === 'black') {
                console.log('black hit')
            playCasinoBlackSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId,
                };
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        } else if (choiceColor === 'redblack') {
                console.log('redblack hit')
            playCasinoRedBlackSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId,
                };
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        } else if (choiceColor === 'redgold') {
                console.log('redgold hit')
            playCasinoRedGoldSound();
                const topHitData = {
                    choice_id: targetCard.getAttribute('id').split('-')[1], // Extract Choice ID
                    color: choiceColor,
                    game_id: gameId,
                };
                // Create the Top Hit
                createTopHit(topHitData);
                $(".start").prop('disabled', true);
                console.log('processed the top hit')
        }
        }

    });

function randomizedContents() {
    const slider = document.querySelector('.slider');
    const children = Array.from(slider.children);

    const targetIndex = children.findIndex(child => child.classList.contains('target-card'));
    let targetCard = null;
    if (targetIndex !== -1) {
        targetCard = children[targetIndex];
    }

    const nonTargetCards = children.filter(child => !child.classList.contains('target-card'));

    for (let i = nonTargetCards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [nonTargetCards[i], nonTargetCards[j]] = [nonTargetCards[j], nonTargetCards[i]];
    }

    slider.innerHTML = '';

    const totalCards = nonTargetCards.length + (targetCard ? 1 : 0);
    for (let i = 0, j = 0; i < totalCards; i++) {
        if (i === targetIndex && targetCard) {
            slider.appendChild(targetCard);
        } else {
            slider.appendChild(nonTargetCards[j]);
            j++;
        }
    }

    console.log("Slider contents randomized without affecting target card position.");
}

    currentSpin++;
    console.log(`Spin #${currentSpin} completed for Button ID: ${buttonId}`);

    if (currentSpin < totalSpins) {
        setTimeout(() => spin(buttonId), buffer);
         setTimeout(() => {
        randomizedContents();
    }, 500);
    } else {
        animationStopped = true;
        console.log(`The spins have ended.`);
        setTimeout(() => {
        showPopup(buttonId);
    }, 250);

                if (!persistSpin) {
                    totalSpins = 1;
                    console.log("persistSpin disabled; reset spins to 1");
                    sessionStorage.setItem("totalSpins", totalSpins);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                } else {
                    const currentSelectionValue = parseInt($(".spin-option.selected").data("value") || 1, 10);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                    setTimeout(() => {
                        $(".spin-option").removeClass("selected active");
                        $(".spin-option[data-value='" + currentSelectionValue + "']")
                            .addClass("selected active");

                        totalSpins = currentSelectionValue;
                        console.log("Reverted spin to:", totalSpins);
                    }, 0);
                }

        $(".spin-option").prop('disabled', false);
    }
}, animationDuration);

}
spin(buttonId);

}

function findSelectedCard() {
    const selector = document.getElementById('selector').getBoundingClientRect();
    let currentSelection = null;

    document.querySelectorAll('.cards').forEach(card => {
        const cardRect = card.getBoundingClientRect();

        if (
            !(selector.right < cardRect.left ||
              selector.left > cardRect.right ||
              selector.bottom < cardRect.top ||
              selector.top > cardRect.bottom)
        ) {
            currentSelection = {
                id: card.id,
                src: card.querySelector('img')?.src || '',
                price: card.dataset.price,
                color: card.dataset.color,
                value: card.dataset.value,
                text: card.dataset.text, // Include additional data like text
            };

            if (card.classList.contains('target-card')) {
                card.classList.add('highlight'); // Apply a class for visual indication
                console.log('Target card landed:', currentSelection);
            }
        }
    });

    if (currentSelection) {
        selectedItems.push(currentSelection);
    }
}

    const sellAudio = new Audio("{% static 'css/sounds/sell_coin.mp3' %}");
    document.querySelectorAll('.sell-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            sellAudio.play();
            console.log('')
            handleAjaxFormSubmission(form);
        });
    });

    function handleAjaxFormSubmission(form) {
        const formData = new FormData(form);
        const actionUrl = form.getAttribute('action');

        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('stock-count').textContent = data.number_of_cards;
            } else {
                console.error(data.error);
            }
        });
    }

 async function showPopup(buttonId) {

if (buttonId === "start") {
  console.log("Show Regular Start");
  window.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log("Sell Imported CSRFToken:", window.csrfToken);

  // Attach the event handler (using delegated binding in case the form is inserted dynamically)
  $(document).ready(function() {
    $(document).on("submit", "#sell-form-" + window.inventory_pk, function(e) {
      e.preventDefault();
      console.log('submitting here'); // Debug output

      var form = $(this);

      // Send the form data via AJAX
      $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        success: function(response) {
          console.log('Sell request succeeded:', response);
          // Instead of refreshing the page, update the relevant part of your page.
          // For example, update a container with the new HTML provided by the server:
          if(response.html) {
            $("#updated-content-container").html(response.html);
          }
          // Alternatively, perform other DOM updates here if needed.
        },
        error: function(error) {

          console.error("Sell request failed:", error);
        }
      });
    });
  });

   textContainer.innerHTML = `
    <h2>Congratulations!</h2>
    <p>You got:</p>
    <div class="cards-container"></div>
    <form id="sell-form-${window.inventory_pk}" action="${window.sellUrl}" method="post" class="ajax-form">
      <input type="hidden" name="csrfmiddlewaretoken" value="${window.csrfToken}">
      <input type="hidden" name="action" value="sell">
      <input type="hidden" name="pk" value="${window.inventory_pk}">
      <button type="submit" class="action-button sell-button" data-inventory_pk="${window.inventory_pk}"
        style="background-color: #c2fbd7; border-radius: 100px; box-shadow: rgba(44, 187, 99, .2) 0 -25px 18px -14px inset, rgba(44, 187, 99, .15) 0 1px 2px, rgba(44, 187, 99, .15) 0 2px 4px, rgba(44, 187, 99, .15) 0 4px 8px, rgba(44, 187, 99, .15) 0 8px 16px, rgba(44, 187, 99, .15) 0 16px 32px; color: green; cursor: pointer; display: inline-block; font-family: CerebriSans-Regular,-apple-system,system-ui,Roboto,sans-serif; padding: 7px 20px; text-align: center; text-decoration: none; transition: all 250ms; border: 0; font-size: 16px; user-select: none; -webkit-user-select: none; touch-action: manipulation;">
          Sell
      </button>
    </form>

  <button class="close" style="">Collect</button>
`;

  } else if (buttonId === "start2") {
      console.log("Show Demo Start");

      textContainer.innerHTML = `
            <h2></h2>
            <p>You would have hit:</p>
            <div class="cards-container"></div>

            <button class="close">I see</button>
        `;
  }


     const cardsContainer = textContainer.querySelector('.cards-container');
     selectedItems.forEach((item, index) => {
         const cardElement = document.createElement('div');
         cardElement.innerHTML = `
            <div class="card-fire" data-color="${item.color}">
              <div class="card-flames">
                <div class="card-flame"></div>
              </div>
            </div>
            <!--<p>ID: ${item.id}</p>
            <p>Nonceword: ${item.nonce}</p>-->
            <img src="${item.src || ''}" alt="${item.id}" width=150 height=225>
            <p>${item.value} 💎</p>
            <!--<p>Lower Nonce: ${item.lowerNonce}</p>
            <p>Upper Nonce: ${item.upperNonce}</p>-->
        `;


            cardsContainer.appendChild(cardElement);

            if (index === 0) {
                const fire = document.querySelector('.fire');
                fire.setAttribute('data-color', item.color);
            }
        });

        popup.style.display = 'block';

        // Trigger the fire animation
        setTimeout(() => {
            const fire = document.querySelector('.fire');
            fire.classList.add('active');
        }, 100);

        const closeBtn = textContainer.querySelector('.close');
        closeBtn.addEventListener('click', () => {




        $(this).addClass("selected");
        totalSpins = parseInt($(this).data("value"));
        sessionStorage.setItem("totalSpins", totalSpins);
        const audio = new Audio('/static/css/sounds/collect.mp3');
        audio.play();

            const fire = document.querySelector('.fire');
            fire.style.opacity = '0';
            document.querySelectorAll('.card-fire').forEach(fire => {
                fire.style.opacity = '0';
            });

            setTimeout(() => {
                popup.style.display = 'none';
            }, 200);

            $(".spin-option").prop('disabled', false);
            $(".start").prop('disabled', false);

 if (!persistSpin) {
                    totalSpins = 1;
                    console.log("persistSpin disabled; reset spins to 1");
                    sessionStorage.setItem("totalSpins", totalSpins);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                } else {
                    const currentSelectionValue = parseInt($(".spin-option.selected").data("value") || 1, 10);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                    setTimeout(() => {
                        $(".spin-option").removeClass("selected active");
                        $(".spin-option[data-value='" + currentSelectionValue + "']")
                            .addClass("selected active");

                        totalSpins = currentSelectionValue;
                        console.log("Reverted spin to:", totalSpins);
                    }, 0);
                }
        });

const sellBtn = textContainer.querySelector('.sell-button');
sellBtn.addEventListener('click', () => {
    const audio = new Audio('/static/css/sounds/collect.mp3');
    audio.play();

    const fire = document.querySelector('.fire');
    fire.style.opacity = '0';
    document.querySelectorAll('.card-fire').forEach(fire => {
        fire.style.opacity = '0';
    });

    setTimeout(() => {
        popup.style.display = 'none';
    }, 0);

    $(".spin-option").prop('disabled', false);
    $(".start").prop('disabled', false);

    if (!persistSpin) {
                    totalSpins = 1;
                    console.log("persistSpin disabled; reset spins to 1");
                    sessionStorage.setItem("totalSpins", totalSpins);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                } else {
                    const currentSelectionValue = parseInt($(".spin-option.selected").data("value") || 1, 10);

                    $(".spin-option").removeClass("selected active");
                    $(".spin-option[data-value='1']").addClass("selected active");

                    setTimeout(() => {
                        $(".spin-option").removeClass("selected active");
                        $(".spin-option[data-value='" + currentSelectionValue + "']")
                            .addClass("selected active");

                        totalSpins = currentSelectionValue;
                        console.log("Reverted spin to:", totalSpins);
                    }, 0);
                }

    // Fetch and update only the .sell.update div without affecting the rest of the page
    setTimeout(() => {
        $.ajax({
            url: window.location.href,
            type: 'GET',
            success: function(response) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = response;
                const newContent = $(tempDiv).find('.sellupdate').html();
                $('.sellupdate').html(newContent);
            },
            error: function(xhr, status, error) {
                console.error("Ajax reload failed: " + xhr.status + " " + xhr.statusText);
            }
        });
    }, 0);
});



    }
});

