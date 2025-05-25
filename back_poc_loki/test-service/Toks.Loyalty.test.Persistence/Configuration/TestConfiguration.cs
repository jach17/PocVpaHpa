// <summary>
// <copyright file="TestConfiguration.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Persistence.Configuration
{
    /// <summary>
    /// TestConfiguration class.
    /// </summary>
    public class TestConfiguration : IEntityTypeConfiguration<TestModel>
    {
        /// <inheritdoc/>
        public void Configure(EntityTypeBuilder<TestModel> builder)
        {
            builder.ToTable("test").HasKey(p => p.Id);

            builder.Property(s => s.Name).HasColumnName("name").IsRequired();

            builder.Property(s => s.Active).HasColumnName("active").IsRequired();

            builder.Property(s => s.Create).HasColumnName("create").IsRequired();

            builder.Property(s => s.User).HasColumnName("user").IsRequired().HasMaxLength(100);

            builder.Property(s => s.UserCreated)
                .HasMaxLength(100)
                .IsRequired();

            builder.Property(s => s.Created)
                .IsRequired();

            builder.Property(s => s.UserModified)
                .HasMaxLength(100);

            builder.Property(s => s.Active)
                .IsRequired();
        }
    }
}
