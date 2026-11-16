import React, { useState } from "react";
import "../styles/login_page.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { CircularProgress } from "react-cssfx-loading";
import CloseIcon from "@mui/icons-material/Close";
import { API_BASE_URL } from "../config/api";

interface LoginPageProps {
    onClose?: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onClose }) => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState<"login" | "signup">("login");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    const [first_name, setfirst_name] = useState("");
    const [last_name, setlast_name] = useState("");
    const [email_id, setemail_id] = useState("");
    const [password, setpassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const handleClose = () => {
        if (onClose) {
            onClose();
            return;
        }
        navigate("/home");
    };

    // Login logic using ID/email and password
    const handleLogin = async () => {
        setErrorMsg(null);
        if (!email_id || !password) {
            setErrorMsg("Please enter both email and password.");
            return;
        }
        if (isSubmitting) return;

        setIsSubmitting(true);

        try {
            const response = await axios.post(`${API_BASE_URL}/auth/login`, {
                email: email_id.trim(),
                password: password
            });

            if (response.data?.success || response.status === 200) {
                localStorage.setItem("email_id", email_id.trim());
                localStorage.setItem("isAuthenticated", "true");
                if (response.data?.user) {
                    localStorage.setItem("user", JSON.stringify(response.data.user));
                }
                navigate("/home");
            }
        } catch (error: any) {
            setIsSubmitting(false);
            const detail = error.response?.data?.detail;
            if (error.response?.status === 404) {
                setErrorMsg("User account not found. Please sign up.");
            } else if (error.response?.status === 401) {
                setErrorMsg(detail || "Invalid password.");
            } else {
                setErrorMsg(detail || "Server error. Please verify backend is running.");
            }
        }
    };

    // Signup logic
    const handleSignup = async () => {
        setErrorMsg(null);
        if (!first_name || !last_name || !email_id || !password) {
            setErrorMsg("Please fill in all required fields.");
            return;
        }
        if (password !== confirmPassword) {
            setErrorMsg("Passwords do not match.");
            return;
        }
        if (isSubmitting) return;

        setIsSubmitting(true);

        try {
            const response = await axios.post(`${API_BASE_URL}/auth/signup`, {
                first_name: first_name.trim(),
                last_name: last_name.trim(),
                email: email_id.trim(),
                password: password
            });

            if (response.data?.success || response.status === 200) {
                localStorage.setItem("email_id", email_id.trim());
                localStorage.setItem("isAuthenticated", "true");
                if (response.data?.user) {
                    localStorage.setItem("user", JSON.stringify(response.data.user));
                }
                navigate("/home");
            }
        } catch (error: any) {
            setIsSubmitting(false);
            const detail = error.response?.data?.detail;
            if (error.response?.status === 409) {
                setErrorMsg("Email is already registered. Please log in.");
            } else {
                setErrorMsg(detail || "Registration failed. Please try again.");
            }
        }
    };

    return (
        <div className="main-login-box">
            <div className="login-card">
                <div className="closeIcon" onClick={handleClose}>
                    <CloseIcon />
                </div>

                {/* Toggle Buttons */}
                <div className="switch-container">
                    <button
                        className={activeTab === "login" ? "active-tab" : ""}
                        onClick={() => {
                            setActiveTab("login");
                            setErrorMsg(null);
                        }}
                    >
                        Login
                    </button>

                    <button
                        className={activeTab === "signup" ? "active-tab" : ""}
                        onClick={() => {
                            setActiveTab("signup");
                            setErrorMsg(null);
                        }}
                    >
                        Signup
                    </button>
                </div>

                {errorMsg && (
                    <div style={{
                        backgroundColor: "rgba(239, 68, 68, 0.15)",
                        border: "1px solid rgba(239, 68, 68, 0.4)",
                        color: "#ef4444",
                        padding: "10px 14px",
                        borderRadius: "8px",
                        fontSize: "13px",
                        marginBottom: "16px",
                        textAlign: "center"
                    }}>
                        {errorMsg}
                    </div>
                )}

                {/* LOGIN FORM */}
                {activeTab === "login" && (
                    <>
                        <div className="email-div">
                            <div className="email-text">Email Address / Login ID</div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address"
                                value={email_id}
                                onChange={(e) => setemail_id(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleLogin()}
                            />
                        </div>

                        <div className="password-div">
                            <div className="password-text">Enter Password</div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setpassword(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleLogin()}
                            />
                        </div>

                        <div className="login-button-div">
                            <button
                                className="login-button"
                                onClick={handleLogin}
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? (
                                    <span className="button-loader">
                                        <CircularProgress size="20px" color="#fff" />
                                    </span>
                                ) : (
                                    "Log In"
                                )}
                            </button>
                        </div>

                        <div className="sign-up-div">
                            <p>
                                Don't have an account?{" "}
                                <b
                                    style={{ cursor: "pointer", color: "#60a5fa" }}
                                    onClick={() => {
                                        setActiveTab("signup");
                                        setErrorMsg(null);
                                    }}
                                >
                                    Sign up
                                </b>
                            </p>
                        </div>
                    </>
                )}

                {/* SIGNUP FORM */}
                {activeTab === "signup" && (
                    <>
                        <div className="firstName-div">
                            <div className="firstName-text">First Name</div>
                            <input
                                className="firstName-input"
                                type="text"
                                placeholder="Enter your first name"
                                value={first_name}
                                onChange={(e) => setfirst_name(e.target.value)}
                            />
                        </div>

                        <div className="lastName-div">
                            <div className="lastName-text">Last Name</div>
                            <input
                                className="lastName-input"
                                type="text"
                                placeholder="Enter your last name"
                                value={last_name}
                                onChange={(e) => setlast_name(e.target.value)}
                            />
                        </div>

                        <div className="email-div">
                            <div className="email-text">Email Address</div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address"
                                value={email_id}
                                onChange={(e) => setemail_id(e.target.value)}
                            />
                        </div>

                        <div className="password-div">
                            <div className="password-text">Password</div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Create a password"
                                value={password}
                                onChange={(e) => setpassword(e.target.value)}
                            />
                        </div>

                        <div className="confirmPassword-div">
                            <div className="password-text">Confirm Password</div>
                            <input
                                className="confirmPassword-input"
                                type="password"
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSignup()}
                            />
                            {confirmPassword && password !== confirmPassword && (
                                <div className="password-mismatch">
                                    Passwords do not match
                                </div>
                            )}
                        </div>

                        <div className="signup-created">
                            <button
                                className="account-created-button"
                                onClick={handleSignup}
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? (
                                    <span className="button-loader">
                                        <CircularProgress size="20px" color="#fff" />
                                    </span>
                                ) : (
                                    "Create Account"
                                )}
                            </button>
                        </div>

                        <div className="already-have-account">
                            <p>
                                Already have an account?{" "}
                                <b
                                    style={{ cursor: "pointer", color: "#60a5fa" }}
                                    onClick={() => {
                                        setActiveTab("login");
                                        setErrorMsg(null);
                                    }}
                                >
                                    Log In
                                </b>
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default LoginPage;
