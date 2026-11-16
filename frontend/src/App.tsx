import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./components/login_page";
import OtpVerify from "./components/otp_verify";
import HomePage from "./components/home_page";

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<LoginPage />} />
                <Route path="/otp_verify" element={<OtpVerify />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default App;
