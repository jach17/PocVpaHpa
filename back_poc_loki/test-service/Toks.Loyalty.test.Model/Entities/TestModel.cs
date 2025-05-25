// <summary>
// <copyright file="TestModel.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>
namespace Toks.Loyalty.test.Model.Entities
{
    /// <summary>
    /// TestModel class.
    /// </summary>
    public class TestModel : SignedModel
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="TestModel"/> class.
        /// </summary>
        public TestModel()
        {
        }

        /// <summary>
        /// Gets or sets Id.
        /// </summary>
        /// <value>
        /// int Id.
        /// </value>
        public int Id { get; set; }

        /// <summary>
        /// Gets or sets Name.
        /// </summary>
        /// <value>
        /// string Name.
        /// </value>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets Active.
        /// </summary>
        /// <value>
        /// bool Active.
        /// </value>
        public bool Active { get; set; }

        /// <summary>
        /// Gets or sets Create.
        /// </summary>
        /// <value>
        /// DateTime Create.
        /// </value>
        public DateTime Create { get; set; }

        /// <summary>
        /// Gets or sets User.
        /// </summary>
        /// <value>
        /// string User.
        /// </value>
        public string User { get; set; }
    }
}
