function joinUs() {
    alert("Thanks for your interest! Please contact us to learn more about joining SASG.");
}


var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-100px";
  }
  prevScrollpos = currentScrollPos;
}

document.addEventListener('click', function(event) {
  const navbar = document.getElementById("navbar");
  if (!event.target.closest('#navbar')) {
    if (navbar.style.top === "0px") {
      navbar.style.top = "-100px";
    } else {
      navbar.style.top = "0";
    }
  }
});


const imageContainers = document.querySelectorAll('.announcement-item');

imageContainers.forEach(container => {
  const img = container.querySelector('img');
  const textDiv = container.querySelector('.announcement-text');

  img.onload = function() { 
    const colorThief = new ColorThief(); 
    const dominantColor = colorThief.getColor(img);

    // Create gradient string (adjust as needed)
    const gradient = `linear-gradient(to right, rgba(${dominantColor.join(',')}, 0.8), rgba(${dominantColor.join(',')}, 0.2))`;

    textDiv.style.background = gradient; 
  }
});

document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('.input-group input');
  
  inputs.forEach(input => {
      // Check if the input has a value on load
      if (input.value) {
          input.classList.add('filled');
      }

      // Add or remove the 'filled' class on input change
      input.addEventListener('input', function() {
          if (input.value) {
              input.classList.add('filled');
          } else {
              input.classList.remove('filled');
          }
      });
  });
});


function openLightbox(url) {
  const lightbox = document.getElementById('lightbox');
  const lightboxContent = document.getElementById('lightbox-content');

  // Show the lightbox
  lightbox.style.display = 'flex';

  // Get lightbox dimensions
  const lightboxWidth = lightbox.offsetWidth;
  const lightboxHeight = lightbox.offsetHeight;

  // If it's a video (check using regex for common video formats)
  const videoExtensions = /\.(mp4|avi|mov|wmv|flv|mkv|webm)$/i;
  if (videoExtensions.test(url)) {
      // Reset content to video
      lightboxContent.innerHTML = `
          <video id="lightbox-video" controls autoplay loop>
              <source id="lightbox-source" src="${url}" type="video/mp4">
              Your browser does not support the video tag.
          </video>`;

      const videoElement = document.getElementById('lightbox-video');
      
      // Wait until video metadata is loaded to calculate dimensions
      videoElement.addEventListener('loadedmetadata', function() {
          const videoWidth = this.videoWidth;
          const videoHeight = this.videoHeight;
          const aspectRatio = videoWidth / videoHeight;

          // Adjust video size based on aspect ratio and lightbox dimensions
          if (aspectRatio > lightboxWidth / lightboxHeight) {
              this.style.width = lightboxWidth * 0.9 + 'px';
              this.style.height = 'auto';
          } else {
              this.style.width = 'auto';
              this.style.height = lightboxHeight * 0.8 + 'px';
          }

          this.play();  // Automatically start video playback
      });
  } 
  // If it's an image
  else {
      // Reset content to image
      lightboxContent.innerHTML = `<img id="lightbox-img" src="${url}" style="">`;

      // Wait until image is loaded to calculate dimensions
      const imageElement = document.getElementById('lightbox-img');
      imageElement.addEventListener('load', function() {
          const imageWidth = this.naturalWidth;
          const imageHeight = this.naturalHeight;
          const aspectRatio = imageWidth / imageHeight;

          // Adjust image size based on aspect ratio and lightbox dimensions
          if (aspectRatio > lightboxWidth / lightboxHeight) {
              this.style.width = lightboxWidth * 0.9 + 'px';
              this.style.height = 'auto';
          } else {
              this.style.width = 'auto';
              this.style.height = lightboxHeight * 0.8 + 'px';
          }
      });
  }

  setTimeout(() => {
      lightbox.classList.add('show');
  }, 10);  // Small delay to allow the display to update before starting the transition
}


function closeLightbox() {
  const lightbox = document.getElementById('lightbox');

  // Remove the show class to trigger the reverse transition
  lightbox.classList.remove('show');
    
  // Wait for the transition to end before hiding the lightbox
  setTimeout(() => {
    // Hide the lightbox
    lightbox.style.display = 'none';

    // Reset content
    document.getElementById('lightbox-content').innerHTML = '';
  }, 400);  // Delay matches the transition duration
}


function playVideo(video) {
  video.play();
  video.addEventListener('ended', function() {
    video.currentTime = 0;
  });
}


function toggleDropdown() {
  const dropdown = document.getElementById("dropdown");
  dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Close dropdown if clicked outside
window.onclick = function(event) {
  if (!event.target.matches('.fab')) {
      const dropdowns = document.getElementsByClassName("dropdown-content");
      for (let i = 0; i < dropdowns.length; i++) {
          const openDropdown = dropdowns[i];
          if (openDropdown.style.display === 'flex') {
              openDropdown.style.display = 'none';
              const fab = document.querySelector('.fab');
              fab.style.transform = 'scale(1)';
          }
      }
  }
};

document.querySelector('.fab').addEventListener('click', function() {
  const dropdownContent = document.querySelector('.dropdown-content');
  dropdownContent.style.display = dropdownContent.style.display === 'flex' ? 'none' : 'flex';
});



function toggleMenu() {
  const sidebar = document.querySelector('.profile-sidebar');
  sidebar.classList.toggle('active');
}