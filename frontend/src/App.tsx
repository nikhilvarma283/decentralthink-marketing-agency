import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'

// Pages (to be implemented in Sprint 1)
const HomePage = () => <div className="p-8"><h1>Welcome to DecentralThink</h1></div>
const LoginPage = () => <div className="p-8"><h1>Login</h1></div>
const SignUpPage = () => <div className="p-8"><h1>Sign Up</h1></div>
const DashboardPage = () => <div className="p-8"><h1>Dashboard</h1></div>
const NotFoundPage = () => <div className="p-8"><h1>404 - Page Not Found</h1></div>

function App() {
  const { isAuthenticated } = useAuth()

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route
            path="/dashboard"
            element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />}
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
