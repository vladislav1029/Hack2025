import React from 'react';
import Header from './components/Header/Header.jsx';
import Home from './pages/Home.jsx';
import Profile from './pages/Profile.jsx';
import PrivateFiles from './pages/PrivateFiles.jsx';
import Files from './pages/Files.jsx';
import CreateProject from './pages/CreateProject.jsx';
import Templates from './pages/Templates.jsx';
import Calendar from './components/Calendar/Calendar.jsx';
import DragToggle from './components/DragToggle/DragToggle.jsx';
import { AuthProvider, useAuth } from './hooks/useAuth.jsx';
import { useDragDrop } from './hooks/useDragDrop.jsx';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// Dashboard component that shows different content based on user role
const RoleBasedDashboard = () => {
  const { user, isAuthenticated, loading } = useAuth();

  // Define default layouts for each role
  const getDefaultLayout = (role) => {
    switch (role) {
      case 0: // Administrator
        return [
          { id: 'projects', type: 'component', title: 'Проекты', component: Home },
          { id: 'profile', type: 'component', title: 'Профиль', component: Profile },
          { id: 'private-files', type: 'component', title: 'Приватные файлы', component: PrivateFiles },
          { id: 'templates', type: 'component', title: 'Шаблоны', component: Templates }
        ];
      case 1: // Manager
        return [
          { id: 'projects', type: 'component', title: 'Управление проектами', component: Home },
          { id: 'private-files', type: 'component', title: 'Приватные файлы', component: PrivateFiles },
          { id: 'profile', type: 'component', title: 'Профиль', component: Profile }
        ];
      case 2: // User
        return [
          { id: 'projects', type: 'component', title: 'Мои проекты', component: Home },
          { id: 'public-files', type: 'component', title: 'Общедоступные файлы', component: Files },
          { id: 'calendar', type: 'component', title: 'Календарь', component: Calendar }
        ];
      default:
        return [];
    }
  };

  const getDashboardTitle = (role) => {
    switch (role) {
      case 0: return 'Панель администратора';
      case 1: return 'Панель менеджера';
      case 2: return 'Панель пользователя';
      default: return 'Панель управления';
    }
  };

  if (loading) {
    return <div className="loading">Загрузка...</div>;
  }

  if (!isAuthenticated) {
    return <div className="loginMessage">Пожалуйста, войдите в систему для доступа к приложению</div>;
  }

  // Initialize drag and drop with role-specific layout
  const { layout, isDragMode, toggleDragMode, handleDragStart, handleDragEnd, handleDragOver, handleDrop } = useDragDrop(
    `dashboard_role_${user?.role}`,
    getDefaultLayout(user?.role)
  );

  const renderDraggableCard = (item, index) => {
    const Component = item.component;
    const isDraggable = isDragMode;

    return (
      <div
        key={`${item.type}_${item.id}`}
        className={`dashboardCard ${isDraggable ? 'draggable' : ''}`}
        draggable={isDraggable}
        onDragStart={(e) => handleDragStart(e, item.id, item.type)}
        onDragEnd={handleDragEnd}
        onDragOver={handleDragOver}
        onDrop={(e) => handleDrop(e, item.id)}
        style={{
          cursor: isDraggable ? 'move' : 'default',
          opacity: isDraggable ? 0.9 : 1,
          transition: 'all 0.2s ease'
        }}
      >
        <h2>{item.title}</h2>
        <Component />
      </div>
    );
  };

  return (
    <div className="dashboardContainer">
      <div className="dashboardHeader">
        <h1>{getDashboardTitle(user?.role)}</h1>
        <DragToggle isDragMode={isDragMode} onToggle={toggleDragMode} />
      </div>

      <div
        className={`dashboardGrid ${isDragMode ? 'drag-mode' : ''}`}
        onDragOver={handleDragOver}
        onDrop={(e) => handleDrop(e, 'end')}
      >
        {layout.map((item, index) => renderDraggableCard(item, index))}
      </div>

      {isDragMode && (
        <div className="dragInstructions">
          Перетаскивайте компоненты для изменения их расположения
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Header />
        <main>
          <RoleBasedDashboard />
        </main>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </div>
    </AuthProvider>
  );
}

export default App;
