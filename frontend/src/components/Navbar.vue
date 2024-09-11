<!-- eslint-disable prettier/prettier -->
<template>
  <nav class="navbar">
    <!-- Sidebar for Desktop -->
    <div class="sidebar" :class="{ 'open': navbarOpen }">
      <button class="sidebar-toggler" @click="toggleNavbar">☰</button>
      <ul class="sidebar-nav">
        <router-link v-if="isAuthenticated" to="/dashboard" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-home"></i>
            <span v-if="navbarOpen">Home</span>
          </li>
        </router-link>
        <router-link v-if="!isAuthenticated" to="/" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-home"></i>
            <span v-if="navbarOpen">Home</span>
          </li>
        </router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span v-if="navbarOpen">Login</span>
          </li>
        </router-link>
        <router-link v-if="!isAuthenticated && isAdmin" to="/adminlogin" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-user-shield"></i>
            <span v-if="navbarOpen">Admin</span>
          </li>
        </router-link>
        <router-link v-if="!isAuthenticated" to="/signup" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span v-if="navbarOpen">Sign Up</span>
          </li>
        </router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/sectionCreation" class="nav-link">
          <li class="nav-item">
            <i class="fa-solid fa-book-bookmark"></i>
            <span v-if="navbarOpen">section Create</span>
          </li>
        </router-link>
        <router-link v-if="isAuthenticated && !isAdmin" to="/profile" class="nav-link">
          <li class="nav-item">
            <i class="fa-regular fa-user"></i>
            <span v-if="navbarOpen">my profile</span>
          </li>
        </router-link>
        <router-link v-if="isAuthenticated && !isAdmin" to="/mybooks" class="nav-link">
          <li class="nav-item">
            <i class="fa-solid fa-book"></i>
            <span v-if="navbarOpen">my book </span>
          </li>
        </router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/libraryregister" class="nav-link">
          <li class="nav-item">
            <i class="fa-solid fa-book"></i>
            <span v-if="navbarOpen">Library Register </span>
          </li>
        </router-link>
        <router-link v-if="isAdmin" to="/admindashboard" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-tachometer-alt"></i>
            <span v-if="navbarOpen">Admin Dashboard</span>
          </li>
        </router-link>
        <router-link v-if="isAdmin" to="/bookcreation" class="nav-link">
          <li class="nav-item">
            <i class="fa-solid fa-folder-plus"></i>
            <span v-if="navbarOpen">Book Create</span>
          </li>
        </router-link>
        <button v-if="isAuthenticated" @click="logout" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span v-if="navbarOpen">Logout</span>
          </li>
        </button>
      </ul>
    </div>
    <!-- Bottom Navbar for Mobile -->
    <div class="bottom-navbar d-lg-none">
      <!-- Bottom Navbar for Mobile -->
      <ul class="bottom-navbar">
        <router-link to="/dashboard" v-if="isAuthenticated" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-home"></i>
          </li><span>Home</span>
        </router-link>
        <router-link to="/" v-if="!isAuthenticated" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-home"></i>
          </li><span>Home</span>
        </router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-sign-in-alt"></i>

          </li><span>Login</span>
        </router-link>
        <router-link v-if="!isAuthenticated && isAdmin" to="/adminlogin" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-user-shield"></i>
            <span>Admin</span>
          </li>
        </router-link>
        <router-link v-if="!isAuthenticated" to="/signup" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-user-plus"></i>

          </li> <span>Sign Up</span>
        </router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/sectionCreation" class="nav-link"
          exact-active-class="active">
          <li class="nav-item">
            <i class="fa-solid fa-book-bookmark"></i>

          </li><span>Section</span>
        </router-link>
        <router-link v-if="isAuthenticated && !isAdmin" to="/search" class="nav-link" exact-active-class="active">
          <li class="nav-item"><i class="fa-solid fa-magnifying-glass"></i></li>
            <span>search</span>
          </router-link>
        <router-link v-if="isAuthenticated && !isAdmin" to="/mybooks" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fa-solid fa-book"></i>
          </li><span>Read</span>
        </router-link>

        <router-link v-if="isAuthenticated && !isAdmin" to="/profile" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fa-regular fa-user"></i>
          </li><span>Profile</span>
        </router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/libraryregister" class="nav-link"
          exact-active-class="active">
          <li class="nav-item">
            <i class="fa-solid fa-book"></i>

          </li><span>Register</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admindashboard" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fas fa-tachometer-alt"></i>

          </li><span>Dashboard</span>
        </router-link>
        <router-link v-if="isAdmin" to="/bookcreation" class="nav-link" exact-active-class="active">
          <li class="nav-item">
            <i class="fa-solid fa-folder-plus"></i>

          </li><span>Book </span>
        </router-link>
        <button v-if="isAuthenticated" @click="logout" class="nav-link">
          <li class="nav-item">
            <i class="fas fa-sign-out-alt"></i>

          </li><span>Logout</span>
        </button>
      </ul>

    </div>
  </nav>
</template>
<!-- eslint-disable prettier/prettier -->
<script>
document.addEventListener('DOMContentLoaded', function () {
  const links = document.querySelectorAll('.bottom-navbar .nav-link');

  links.forEach(link => {
    link.addEventListener('click', function () {
      links.forEach(link => link.classList.remove('active'));
      this.classList.add('active');
    });
  });
});
</script>
<!-- eslint-disable prettier/prettier -->
<script>
import axios from "axios";

export default {
  data() {
    return {
      isAuthenticated: false,
      isAdmin: false,
      navbarOpen: false,
    };
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen;
    },
    async logout() {
            try {
                const response = await axios.post("/logout", {}, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
                        'Content-Type': 'application/json'  // Specify content type if needed
                    },
                    withCredentials: true
                });
                if (response.status === 200) {
                    this.isAuthenticated = false;
                    this.isAdmin = false;
                    localStorage.removeItem("userRole");
                    localStorage.removeItem("accessToken");
                    this.$router.push("/login");
                }
            } catch (error) {
                this.isAuthenticated = false;
                    this.isAdmin = false;
                    localStorage.removeItem("userRole");
                    localStorage.removeItem("accessToken");
                    this.$router.push("/login");
                }
            },
    checkUserRole() {
      const userRole = localStorage.getItem("userRole");
      const accessToken = localStorage.getItem("accessToken");

      if (userRole && accessToken) {
        this.isAuthenticated = true;
        this.isAdmin = userRole === "admin";
      } else {
        this.isAuthenticated = false;
        this.isAdmin = false;
      }
    },
  },
  created() {
    // Check user role and authentication status when component is created
    this.checkUserRole();

    // Listen for authentication status updates
    this.$root.$on('updateAuthStatus', (isAuthenticated, isAdmin) => {
      this.isAuthenticated = isAuthenticated;
      this.isAdmin = isAdmin;
      this.checkUserRole(); // Ensure user role is checked whenever auth status changes
    });
  },
};



// created() {
// axios
//   .get('/checkSession', { withCredentials: true })
//   .then((response) => {
//     console.log('checkSession response:', response.data);  // Log for debugging
//     const { isAuthenticated, isAdmin } = response.data;
//     this.isAuthenticated = isAuthenticated;
//     localStorage.setItem("userRole", isAdmin ? "admin" : "user");
//     this.checkUserRole();
//   })
//   .catch((error) => {
//     console.error("Session check error:", error);
//     this.isAuthenticated = false;
//     this.isAdmin = false;
//   });

// this.$root.$on('updateAuthStatus', (isAuthenticated, isAdmin) => {
//   this.isAuthenticated = isAuthenticated;
//   this.isAdmin = isAdmin;
//   this.checkUserRole();
// });
// },
</script>
<!-- eslint-disable prettier/prettier -->

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Amaranth&family=Kdam+Thmor+Pro&family=Lato&family=Poppins&family=Rubik&display=swap');

.navbar {
  display: flex;
  flex-direction: column;
  height: 100%;
  box-shadow: 0 0 3px rgb(118, 118, 118);
  border-radius: 20px;
  background-color: #C8ACD6;
}

.sidebar {
  display: flex;
  flex-direction: column;
  width: 60px;
  max-height: 100%;
  transition: width 0.3s ease;
}

.sidebar.open {
  width: 250px;
}

.sidebar-toggler {
  background-color: rgba(255, 255, 255, 0);
  color:#433D8B;
  border: none;
  font-size: 24px;
  padding: 10px;
  cursor: pointer;
}

.sidebar-nav {
  list-style-type: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.sidebar-nav .nav-link {
  padding: 15px;
  text-decoration: none;
  color: #2E236C;
  display: flex;
  align-items: center;
}

.sidebar-nav .nav-item {
  padding: 10px;
  display: flex;
  align-items: center;
}

.sidebar-nav .nav-item i {
  margin-right: 10px;
}

.sidebar-nav .nav-link:hover {
  background-color: #2E236C;
  color: aliceblue;
}

.bottom-navbar ul {
  background: linear-gradient(135deg,#433D8B,#1B1A55);
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #eee;
  padding-left: 0;
  margin: 0;
  position: fixed;
  bottom: 0;
  width: 100%;
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.bottom-navbar .nav-link {
  list-style-type: none;
  text-align: center;
  padding: 10px 0;
  color: #ffffff;
  text-decoration: none;
  transition: transform 0.3s ease, color 0.3s ease;
}

.bottom-navbar .nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.2em;
  transition: transform 0.3s ease;
  border-radius: 50%;
  padding: 10px;
}

.bottom-navbar
.bottom-navbar .nav-link.active .nav-item {
  transform: scale(1.25) translateY(-0.7em);
  background: linear-gradient(135deg,#433D8B,#1B1A55);
  color: #fff;
  border: 5px solid #ffffff;
}

.bottom-navbar .nav-item i {
  margin-bottom: 5px;
}

/* Responsive Design */
@media (max-width: 1024px) {

  .sidebar.open {
    width: 250px;
    /* Keep the open width for better usability on larger screens */
  }
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
    /* Hide sidebar on small screens */
  }

  .bottom-navbar {
    display: flex;
    /* Show bottom navbar on small screens */
  }
  .section1 {
    display: flex;
    flex-wrap: wrap;
  }
}

@media (min-width: 769px) {
  .bottom-navbar {
    display: none;
    /* Hide bottom navbar on larger screens */
  }
}

</style>
