import Vue from "vue";
import VueRouter from "vue-router";
import LoginView from "@/views/LoginView.vue";
import SignupView from "@/views/SignupView.vue";
import HomeView from "@/views/HomeView.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import DashboardView from "@/views/DashboardView.vue";
import AdminLogin from "@/views/AdminLogin.vue";
import BookCreation from "@/views/BookCreation.vue";
import UserProfile from "@/views/UserProfile.vue";
import Editprofile from "@/views/Editprofile.vue";
import BookView from "@/views/BookView.vue";
import SelectedBook from "@/components/selectedBook.vue";
import LibraryRegister from "@/views/LibraryRegister.vue";
import MyBooks from "@/views/MyBooks.vue";
import BookEdit from "@/views/BookEdit.vue";
import SectionCreation from "@/views/SectionCreation.vue";
import SectionPage from "@/views/SectionPage.vue";
import AddBook from "@/views/addBook.vue";
import SearchView from "@/views/SearchView.vue";
import Editsection from "@/views/Editsection.vue";
import AllUsers from "@/views/AllUsers.vue";
import AllBooks from "@/views/AllBooks.vue";
import AllSection from "@/views/AllSection.vue";
import downloads from "@/views/downloads.vue";
import PurchasePage from "@/views/purchasePage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/adminlogin",
    name: "adminlogin",
    component: AdminLogin,
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
  },
  {
    path: "/adminDashboard",
    name: "adminDashboard",
    component: AdminDashboard,
  },
  {
    path: "/dashboard",
    name: "dashboardview",
    component: DashboardView,
  },
  {
    path: "/purchase/:bookId?",
    name: "Purchase",
    component: PurchasePage,
  },
  {
    path: "/bookcreation",
    name: "bookcreation",
    component: BookCreation,
  },
  {
    path: "/profile/:userId?",
    name: "profile",
    component: UserProfile,
  },
  {
    path: "/bookspage/:bookId?",
    name: "EbookPage",
    component: BookView,
  },
  {
    path: "/bookspage/:bookId?",
    name: "SelectedBook",
    component: SelectedBook,
  },
  {
    path: "/requestbook/:bookId?",
    name: "SelectedBook",
    component: SelectedBook,
  },
  {
    path: "/AllUsers",
    name: "AllUsers",
    component: AllUsers,
  },
  {
    path: "/downloads",
    name: "downloads",
    component: downloads,
  },
  {
    path: "/AllSection",
    name: "AllSection",
    component: AllSection,
  },
  {
    path: "/AllBooks",
    name: "AllBooks",
    component: AllBooks,
  },
  {
    path: "/libraryregister/approvebook/:requestId?",
    name: "approvebook",
    component: LibraryRegister,
  },
  {
    path: "/libraryregister/retrieve/:requestId?",
    name: "retrieve",
    component: LibraryRegister,
  },
  {
    path: "/libraryregister",
    name: "LibraryRegister",
    component: LibraryRegister,
  },
  {
    path: "/requestreject/",
    name: "rejectrequest",
    component: LibraryRegister,
  },
  {
    path: "/Editprofile/:userId?",
    name: "Editprofile",
    component: Editprofile,
  },
  {
    path: "/mybooks/",
    name: "MyBooks",
    component: MyBooks,
  },
  {
    path: "/ratebook/",
    name: "EbookPage",
    component: BookView,
  },
  {
    path: "/EditBook/:bookId?",
    name: "EditBook",
    component: BookEdit,
  },
  {
    path: "/sectionCreation",
    name: "SectionCreation",
    component: SectionCreation,
  },
  {
    path: "/sectionspage/:sectionId?",
    name: "SectionPage",
    component: SectionPage,
  },
  {
    path: "/AddBooksToSection/:sectionId?",
    name: "AddBooks",
    component: AddBook,
  },
  {
    path: "/searchBooks",
    name: "searchBooks",
    component: AddBook,
  },
  {
    path: "/Editsections/:sectionId?",
    name: "Editsections",
    component: Editsection,
  },
  {
    path: "/search",
    name: "search",
    component: SearchView,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
