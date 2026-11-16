import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/home_page.css";
import { API_BASE_URL } from "../config/api";

interface ApiKeyItem {
    id: number;
    api_key_name: string;
    created_at: string | null;
    last_used_at: string | null;
    is_active: boolean;
    has_password: boolean;
}

const HomePage: React.FC = () => {
    const navigate = useNavigate();
    const [userEmail, setUserEmail] = useState<string | null>(null);
    const [keys, setKeys] = useState<ApiKeyItem[]>([]);
    const [isLoadingKeys, setIsLoadingKeys] = useState(false);

    // Modal states
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [showRetrieveModal, setShowRetrieveModal] = useState(false);

    // Create Key form states
    const [createKeyName, setCreateKeyName] = useState("");
    const [createKeyPassword, setCreateKeyPassword] = useState("");
    const [isCreatingKey, setIsCreatingKey] = useState(false);
    const [createdKeyResult, setCreatedKeyResult] = useState<{ id: number; key: string; name: string } | null>(null);
    const [createError, setCreateError] = useState<string | null>(null);

    // Retrieve Key form states
    const [retrieveKeyId, setRetrieveKeyId] = useState("");
    const [retrieveKeyPassword, setRetrieveKeyPassword] = useState("");
    const [isRetrievingKey, setIsRetrievingKey] = useState(false);
    const [retrievedKeyResult, setRetrievedKeyResult] = useState<{ id: number; key: string; name: string } | null>(null);
    const [retrieveError, setRetrieveError] = useState<string | null>(null);

    // Copy to clipboard notification
    const [copySuccess, setCopySuccess] = useState<string | null>(null);

    const fetchUserKeys = useCallback(async (email: string) => {
        setIsLoadingKeys(true);
        try {
            const response = await axios.get(`${API_BASE_URL}/user-keys`, {
                params: { email }
            });
            if (Array.isArray(response.data)) {
                setKeys(response.data);
            }
        } catch (err) {
            console.warn("Could not load user keys:", err);
        } finally {
            setIsLoadingKeys(false);
        }
    }, []);

    useEffect(() => {
        const storedEmail = localStorage.getItem("email_id");
        if (!storedEmail) {
            navigate("/login");
            return;
        }
        setUserEmail(storedEmail);
        fetchUserKeys(storedEmail);
    }, [navigate, fetchUserKeys]);

    const handleLogout = () => {
        localStorage.removeItem("email_id");
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("user");
        navigate("/login");
    };

    const handleCreateKey = async (e: React.FormEvent) => {
        e.preventDefault();
        setCreateError(null);
        if (!createKeyName.trim()) {
            setCreateError("Please enter a name for your API key.");
            return;
        }
        if (!userEmail) return;

        setIsCreatingKey(true);
        try {
            const payload = {
                email: userEmail,
                api_key_name: createKeyName.trim(),
                password: createKeyPassword.trim() || undefined
            };
            const response = await axios.post(`${API_BASE_URL}/create-api-keys`, payload);
            const data = response.data;

            setCreatedKeyResult({
                id: data.id,
                key: data.key_generation,
                name: data.api_key_name || createKeyName.trim()
            });

            setCreateKeyName("");
            setCreateKeyPassword("");
            fetchUserKeys(userEmail);
        } catch (err: any) {
            const detail = err.response?.data?.detail;
            setCreateError(detail || "Failed to create API key.");
        } finally {
            setIsCreatingKey(false);
        }
    };

    const handleRetrieveKey = async (e: React.FormEvent) => {
        e.preventDefault();
        setRetrieveError(null);
        if (!retrieveKeyId) {
            setRetrieveError("Please enter the API Key ID.");
            return;
        }

        setIsRetrievingKey(true);
        try {
            const payload = {
                id: parseInt(retrieveKeyId, 10),
                password: retrieveKeyPassword,
                email: userEmail
            };
            const response = await axios.post(`${API_BASE_URL}/retrieve-api-key`, payload);
            const data = response.data;

            setRetrievedKeyResult({
                id: data.id,
                key: data.API_Key_data,
                name: data.api_key_name || `Key #${data.id}`
            });
        } catch (err: any) {
            const detail = err.response?.data?.detail;
            setRetrieveError(detail || "Failed to retrieve API key. Check ID and password.");
        } finally {
            setIsRetrievingKey(false);
        }
    };

    const copyToClipboard = (text: string, label: string) => {
        navigator.clipboard.writeText(text);
        setCopySuccess(label);
        setTimeout(() => setCopySuccess(null), 2500);
    };

    const openRetrieveForKey = (keyId: number) => {
        setRetrieveKeyId(keyId.toString());
        setRetrieveKeyPassword("");
        setRetrieveError(null);
        setRetrievedKeyResult(null);
        setShowRetrieveModal(true);
    };

    return (
        <div className="home-container">
            <div className="dashboard-wrapper">
                {/* Header */}
                <div className="dashboard-header">
                    <div className="header-user-info">
                        <span className="home-badge">Login Successful</span>
                        <h1>API Key Management Portal</h1>
                        <p className="home-subtitle">
                            Authenticated as <strong className="user-email">{userEmail}</strong>
                        </p>
                    </div>
                    <button className="dashboard-logout-btn" onClick={handleLogout}>
                        Log Out
                    </button>
                </div>

                {/* Primary Action Buttons */}
                <div className="dashboard-actions-banner">
                    <div className="action-card create-action-card">
                        <div className="action-card-icon">➕</div>
                        <div className="action-card-text">
                            <h3>Create New API Key</h3>
                            <p>Generate a secure UUID key encrypted in the database with AES-256.</p>
                        </div>
                        <button
                            className="primary-btn create-btn"
                            onClick={() => {
                                setCreateError(null);
                                setCreatedKeyResult(null);
                                setShowCreateModal(true);
                            }}
                        >
                            Create API Key
                        </button>
                    </div>

                    <div className="action-card retrieve-action-card">
                        <div className="action-card-icon">🔍</div>
                        <div className="action-card-text">
                            <h3>Retrieve API Key</h3>
                            <p>Decrypt and view an existing API key using your key ID and password.</p>
                        </div>
                        <button
                            className="primary-btn retrieve-btn"
                            onClick={() => {
                                setRetrieveError(null);
                                setRetrievedKeyResult(null);
                                setShowRetrieveModal(true);
                            }}
                        >
                            Retrieve API Key
                        </button>
                    </div>
                </div>

                {/* API Keys Table */}
                <div className="keys-section">
                    <div className="keys-section-header">
                        <h2>Your API Keys</h2>
                        <button
                            className="refresh-btn"
                            onClick={() => userEmail && fetchUserKeys(userEmail)}
                            disabled={isLoadingKeys}
                        >
                            {isLoadingKeys ? "Refreshing..." : "↻ Refresh"}
                        </button>
                    </div>

                    {keys.length === 0 ? (
                        <div className="empty-keys-box">
                            <p>You haven't generated any API keys yet.</p>
                            <button
                                className="small-action-btn"
                                onClick={() => {
                                    setCreateError(null);
                                    setCreatedKeyResult(null);
                                    setShowCreateModal(true);
                                }}
                            >
                                Generate your first key
                            </button>
                        </div>
                    ) : (
                        <div className="keys-table-container">
                            <table className="keys-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Key Name</th>
                                        <th>Status</th>
                                        <th>Protection</th>
                                        <th>Created</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {keys.map((k) => (
                                        <tr key={k.id}>
                                            <td className="key-id-cell">#{k.id}</td>
                                            <td className="key-name-cell">{k.api_key_name}</td>
                                            <td>
                                                <span className={`status-pill ${k.is_active ? "active" : "inactive"}`}>
                                                    {k.is_active ? "Active" : "Disabled"}
                                                </span>
                                            </td>
                                            <td>
                                                <span className="protection-pill">
                                                    {k.has_password ? "🔒 Protected" : "🔓 Open"}
                                                </span>
                                            </td>
                                            <td className="date-cell">
                                                {k.created_at ? new Date(k.created_at).toLocaleDateString() : "—"}
                                            </td>
                                            <td>
                                                <button
                                                    className="table-retrieve-btn"
                                                    onClick={() => openRetrieveForKey(k.id)}
                                                >
                                                    Retrieve Key
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>

            {/* CREATE API KEY MODAL */}
            {showCreateModal && (
                <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Create New API Key</h3>
                            <button className="modal-close-btn" onClick={() => setShowCreateModal(false)}>✕</button>
                        </div>

                        {!createdKeyResult ? (
                            <form onSubmit={handleCreateKey}>
                                <div className="form-group">
                                    <label>API Key Name *</label>
                                    <input
                                        type="text"
                                        placeholder="e.g., Development Server, Mobile App"
                                        value={createKeyName}
                                        onChange={(e) => setCreateKeyName(e.target.value)}
                                        required
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Key Protection Password (Optional)</label>
                                    <input
                                        type="password"
                                        placeholder="Set a password to encrypt/lock retrieval"
                                        value={createKeyPassword}
                                        onChange={(e) => setCreateKeyPassword(e.target.value)}
                                    />
                                    <small className="field-hint">
                                        If specified, this password will be required each time you retrieve the key.
                                    </small>
                                </div>

                                {createError && <div className="modal-error">{createError}</div>}

                                <div className="modal-actions">
                                    <button
                                        type="button"
                                        className="btn-secondary"
                                        onClick={() => setShowCreateModal(false)}
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="btn-primary"
                                        disabled={isCreatingKey}
                                    >
                                        {isCreatingKey ? "Generating..." : "Generate Key"}
                                    </button>
                                </div>
                            </form>
                        ) : (
                            <div className="key-created-success">
                                <div className="success-icon">✓</div>
                                <h4>API Key Created Successfully!</h4>
                                <p className="key-name-label">Key Name: <strong>{createdKeyResult.name}</strong> (ID: #{createdKeyResult.id})</p>

                                <div className="key-display-box">
                                    <code>{createdKeyResult.key}</code>
                                    <button
                                        className="copy-btn"
                                        onClick={() => copyToClipboard(createdKeyResult.key, "created")}
                                    >
                                        {copySuccess === "created" ? "Copied! ✓" : "Copy"}
                                    </button>
                                </div>

                                <div className="warning-notice">
                                    ⚠️ Please copy and store this API key safely now. The raw key is encrypted in the database using AES-256 and cannot be viewed in plain text without retrieval authorization.
                                </div>

                                <button
                                    className="btn-primary full-width"
                                    onClick={() => setShowCreateModal(false)}
                                >
                                    Done
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* RETRIEVE API KEY MODAL */}
            {showRetrieveModal && (
                <div className="modal-overlay" onClick={() => setShowRetrieveModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Retrieve API Key</h3>
                            <button className="modal-close-btn" onClick={() => setShowRetrieveModal(false)}>✕</button>
                        </div>

                        {!retrievedKeyResult ? (
                            <form onSubmit={handleRetrieveKey}>
                                <div className="form-group">
                                    <label>API Key ID *</label>
                                    <input
                                        type="number"
                                        placeholder="Enter Key ID (e.g. 1)"
                                        value={retrieveKeyId}
                                        onChange={(e) => setRetrieveKeyId(e.target.value)}
                                        required
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Key Password</label>
                                    <input
                                        type="password"
                                        placeholder="Enter the password set for this key"
                                        value={retrieveKeyPassword}
                                        onChange={(e) => setRetrieveKeyPassword(e.target.value)}
                                    />
                                    <small className="field-hint">
                                        Required if a protection password was set during or after key creation.
                                    </small>
                                </div>

                                {retrieveError && <div className="modal-error">{retrieveError}</div>}

                                <div className="modal-actions">
                                    <button
                                        type="button"
                                        className="btn-secondary"
                                        onClick={() => setShowRetrieveModal(false)}
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="btn-primary"
                                        disabled={isRetrievingKey}
                                    >
                                        {isRetrievingKey ? "Decrypting..." : "Retrieve & Decrypt"}
                                    </button>
                                </div>
                            </form>
                        ) : (
                            <div className="key-retrieved-success">
                                <div className="success-icon">🔓</div>
                                <h4>API Key Decrypted Successfully!</h4>
                                <p className="key-name-label">Key: <strong>{retrievedKeyResult.name}</strong> (ID: #{retrievedKeyResult.id})</p>

                                <div className="key-display-box">
                                    <code>{retrievedKeyResult.key}</code>
                                    <button
                                        className="copy-btn"
                                        onClick={() => copyToClipboard(retrievedKeyResult.key, "retrieved")}
                                    >
                                        {copySuccess === "retrieved" ? "Copied! ✓" : "Copy"}
                                    </button>
                                </div>

                                <button
                                    className="btn-primary full-width"
                                    onClick={() => setShowRetrieveModal(false)}
                                >
                                    Close
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;
