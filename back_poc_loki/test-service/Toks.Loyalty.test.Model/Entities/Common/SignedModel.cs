// <summary>
// <copyright file="SignedModel.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Model.Entities.Common
{
    /// <summary>
    /// Class BaseSignedModel.
    /// </summary>
    public abstract class SignedModel
    {
        /// <summary>
        /// Gets or sets UserCreated.
        /// </summary>
        /// <value>
        /// String UserCreated.
        /// </value>
        public string UserCreated { get; set; }

        /// <summary>
        /// Gets or sets Created.
        /// </summary>
        /// <value>
        /// DateTime Created.
        /// </value>
        public DateTime Created { get; set; }

        /// <summary>
        /// Gets or sets UserModified.
        /// </summary>
        /// <value>
        /// String UserModified.
        /// </value>
        public string UserModified { get; set; }

        /// <summary>
        /// Gets or sets Modified.
        /// </summary>
        /// <value>
        /// DateTime Modified.
        /// </value>
        public DateTime? Modified { get; set; }

        /// <summary>
        /// Gets or sets a value indicating whether gets or sets Active.
        /// </summary>
        /// <value>
        /// Bool Active.
        /// </value>
        public bool Active { get; set; }
    }
}