<template>
  <div class="home">
    <div class="landingPage">
      <!-- Left Section with Text and Buttons -->
      <div class="contentMain">
        <div class="landLeft">
          <div class="content">
            <h3>Live</h3>
            <p class="TextLand">A new life</p>
            <div class="NameLand">
              <p class="TextLand">With every</p>
              <h3 class="BookTEXTLand">Book</h3>
            </div>
            <div class="buttons">
              <button class="login-btn" @click="navigateToLogin">Login</button>
              <button class="signup-btn" @click="navigateToSignup">
                Sign Up
              </button>
            </div>
          </div>
        </div>

        <!-- Right Section with Glowing Book Image -->
        <div class="landRight">
          <div class="bookshelf">
            <div class="book">
              <div class="book1 bookLine">
                <img
                  src="@/assets/img1.png"
                  alt="Book Image"
                  class="imageBook"
                />
              </div>
              <div class="book1 bookLine">
                <img
                  src="@/assets/img2.png"
                  alt="Book Image"
                  class="imageBook"
                />
              </div>
              <div class="book1 bookLine">
                <img
                  src="@/assets/img3.png"
                  alt="Book Image"
                  class="imageBook"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="sub_content">
        <div class="quote">
          "A room without books is like <br />
          a body without a soul." - Cicero
        </div>
        <div class="landing_page_bottom">
          <div class="dataCard">
            <h2>Books</h2>
            <span>100K+</span>
          </div>
          <div class="dataCard">
            <h2>sections</h2>
            <span>1K+</span>
          </div>
          <div class="dataCard">
            <h2>Users</h2>
            <span>100K+</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    navigateToLogin() {
      this.$router.push("/login");
    },
    navigateToSignup() {
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
.home {
  height: 100vh;
  color: #fff;
  font-family: Inter, sans-serif;
  background-image: radial-gradient(circle, #433d8b, #17153b);
}
.NameLand {
  display: flex;
  flex-direction: row;
  margin: 20px;
}
.landingPage {
  height: 100vh;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
h3 {
  font-size: 100px;
  color: rgb(238, 125, 221);
  font-weight: bold;
  font-family: "Sofia", sans-serif;
}
.BookTEXTLand {
  margin-left: 20px;
}

.TextLand {
  font-size: 50px;
  font-weight: bold;
}
.landLeft {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60%;
}

.contentMain {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 150vh;
}
.landRight {
  display: flex;
  position: relative;
  flex: 1 1 20%;
  align-content: center;
  flex-wrap: wrap;
  right: -400px;
}
.content {
  text-align: left;
}

.title {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.quote {
  font-size: 2.5rem;
  font-style: italic;
  margin: 2rem;
}

.sub_content {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 40px;
  width: 100%;
}
.landing_page_bottom {
  width: 50%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.dataCard {
  margin: 30px;
  border: solid 4px rgb(215, 111, 222);
  padding: 30px;
  border-radius: 20px;
  background: #ffffff1a;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.dataCard span {
  color: transparent;
  font-size: 40px;
  font-weight: bold;
  background-image: linear-gradient(
    to right,
    #462523 0%,
    #cb9b51 22%,
    #f6e27a 45%,
    #f6f3c0 50%,
    #f6e27a 55%,
    #cb9b51 78%,
    #462523 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  animation: shineEffect 25s linear infinite;
}

@keyframes shineEffect {
  0% {
    background-position: -200% center;
  }
  50% {
    background-position: 200% center;
  }
  100% {
    background-position: -200% center;
  }
}

.buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.login-btn,
.signup-btn {
  padding: 0.75rem 2rem;
  font-size: 1.2rem;
  color: #2e3032;
  background-color: rgb(238, 125, 221);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.login-btn:hover,
.signup-btn:hover {
  transform: scale(1.05);
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
}

.book {
  display: flex;
  flex-direction: row;
  align-items: center;
  /* Negative gap for overlapping effect */
}
.bookLine {
  margin: -190px;
}
.book1 {
  z-index: 1;
}
.book2 {
  z-index: 2;
}
.imageBook,
.imageBook2 {
  width: 300px;
  padding: -20px;
  height: auto;
  transition: transform 0.3s, z-index 0.3s;
  z-index: 1;
}

.imageBook2 {
  z-index: 2; /* Adjust z-index to control stacking order */
}

.imageBook:hover,
.imageBook2:hover {
  transform: translateY(-70px);
  z-index: 10;
}

@media (max-width: 1024px) {
  .landRight {
    display: None;
  }
}

@media (max-width: 768px) {
  .landRight {
    display: None;
  }
  .home {
    height: 160vh;
    width: 100%;
  }
  h3 {
    font-size: 50px;
    color: rgb(238, 125, 221);
    font-weight: bold;
    font-family: "Sofia", sans-serif;
  }
  .BookTEXTLand {
    margin-left: 20px;
  }

  .TextLand {
    font-size: 30px;
    font-weight: bold;
  }
  .landLeft {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .quote {
    font-size: 1.5rem;
    font-style: italic;
    margin: 2rem;
  }
}
</style>
